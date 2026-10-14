"""Real Windows named pipe transport (tasks 1.4-1.6).

Wraps the pywin32 named-pipe API so the agent service can talk to X4's
``sn_mod_support_apis`` MESSAGE-mode pipe.  X4 is the pipe *client*; the
Python agent service is the *server* and owns the pipe.

pywin32 is imported lazily so that importing this module (and running the
in-memory tests/smoke) succeeds without it and without Windows.  A clear
``TransportError`` is raised at call time if the dependency is missing.

Message framing is the OS MESSAGE-mode boundary: each ``send`` writes one
complete pipe message, each ``recv`` reads exactly one pipe message.

All access to the pipe file handle is serialised through a single I/O thread
that owns the handle and performs reads and writes in order.  This is not a
stylistic choice: on Windows, a ``ReadFile`` left pending by one thread and a
``WriteFile`` from another thread on the *same* named-pipe handle deadlock (a
blocked reader occupies the pipe's read side).  The I/O thread is the only
thing that ever calls ``ReadFile``/``WriteFile`` on the handle, so the
pipe is never operated on concurrently.
"""

from __future__ import annotations

import os
import queue
import threading
import time
from typing import Optional

from base import (
    ConnectionState,
    Transport,
    TransportDisconnectedError,
    TransportError,
)
from runtime_user import require_avalakh

# Buffer must exceed the largest single message (MAX_MESSAGE_BYTES = 64 KiB).
_PIPE_READ_BUFFER = 128 * 1024  # 128 KiB

# Sentinels / helpers for the I/O queue.
_SHUTDOWN = object()


class _Request:
    """A single read or write operation to be executed by the I/O thread.

    The I/O thread fills ``result``/``error`` and then sets ``done``, which
    is what the caller of ``send``/``recv`` waits on (with a timeout)."""

    __slots__ = ("kind", "data", "result", "error", "done", "timeout_seconds", "timed_out")

    def __init__(self, kind: str, data: Optional[str] = None, timeout_seconds: float = 0) -> None:
        self.kind = kind            # "send" or "recv"
        self.data = data            # message to send (kind == "send")
        self.result: Optional[str] = None  # decoded message (kind == "recv")
        self.error: Optional[object] = None
        self.done = threading.Event()
        self.timeout_seconds = timeout_seconds
        self.timed_out = False


def _pywin32():
    """Lazily import pywin32; raise a clear error if unavailable."""
    try:
        import win32file
        import win32pipe
        import winerror  # noqa: F401

        return win32file, win32pipe, winerror
    except ImportError as exc:
        raise TransportError(
            "pywin32 is required for the real named-pipe transport (pip install pywin32)"
        ) from exc


def _pipe_path(name: str) -> str:
    return "\\\\.\\pipe\\" + name


class NamedPipeServer(Transport):
    """A MESSAGE-mode named pipe server (the X4_Python_Pipe_Server role)."""

    def __init__(self, pipe_name: str = "x4_topmanager_agent") -> None:
        self.pipe_name = pipe_name
        self._file = None
        self._connected = False
        self._closed = False
        self._queue: "queue.Queue[_Request]" = queue.Queue()
        self._io_thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        """Create and arm the pipe, then wait for the X4 client to connect."""
        require_avalakh()
        wfile, wpipe, werr = _pywin32()
        if not os.name.startswith("nt"):
            raise TransportError("named pipes are Windows-only")
        handle = wpipe.CreateNamedPipe(
            self._pipe_path(),
            wpipe.PIPE_ACCESS_DUPLEX,
            wpipe.PIPE_TYPE_MESSAGE | wpipe.PIPE_READMODE_MESSAGE | wpipe.PIPE_WAIT,
            1,  # one concurrent client (X4)
            _PIPE_READ_BUFFER,
            _PIPE_READ_BUFFER,
            300,
            None,
        )
        # Block until X4 (the client) connects. A failed handshake must not
        # leave the server name/handle occupied for the next reconnect.
        try:
            wpipe.ConnectNamedPipe(handle, None)
        except Exception as exc:
            if getattr(exc, "winerror", None) != werr.ERROR_PIPE_CONNECTED:
                wfile.CloseHandle(handle)
                raise
        self._file = handle
        self._queue = queue.Queue()
        self._closed = False
        self._connected = True
        self._io_thread = threading.Thread(target=self._io_loop, daemon=True)
        self._io_thread.start()

    def _pipe_path(self) -> str:
        return _pipe_path(self.pipe_name)

    def _io_loop(self) -> None:
        """The single thread that owns the pipe handle.  Reads and writes are
        executed strictly here and strictly in order, so the Windows named
        pipe never sees two simultaneous operations on the same handle."""
        wfile, wpipe, _ = _pywin32()
        while self._file is not None and not self._closed:
            try:
                req = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
            if req is _SHUTDOWN:
                break
            if req.kind == "send":
                try:
                    wfile.WriteFile(self._file, req.data.encode("utf-8"))
                except Exception as exc:  # noqa: BLE001
                    req.error = exc
            elif req.kind == "recv":
                try:
                    # A timed-out blocking ReadFile would remain queued and
                    # steal the *next* command's response. Peek until ready,
                    # then perform exactly one complete MESSAGE-mode read.
                    deadline = time.monotonic() + req.timeout_seconds
                    while not self._closed:
                        _, available, _ = wpipe.PeekNamedPipe(self._file, 1)
                        if available:
                            _, data = wfile.ReadFile(self._file, _PIPE_READ_BUFFER)
                            break
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            req.timed_out = True
                            break
                        time.sleep(min(0.02, remaining))
                    else:
                        req.error = TransportDisconnectedError("pipe closed")
                except Exception as exc:  # noqa: BLE001
                    req.error = exc
                    self._closed = True
                else:
                    if req.timed_out or req.error is not None:
                        pass
                    elif data:
                        req.result = data.decode("utf-8", errors="replace")
                    else:
                        # Empty read == EOF: the peer closed the write side.
                        self._closed = True
            else:
                req.done.set()
                continue
            req.done.set()
        # Clean up the handle on exit (the io thread is its owner).
        if self._file is not None:
            try:
                wfile.FlushFileBuffers(self._file)
            except Exception:
                pass
            try:
                wpipe.DisconnectNamedPipe(self._file)
            except Exception:
                pass
            try:
                wfile.CloseHandle(self._file)
            except Exception:
                pass
            self._file = None

    def _mark_disconnected(self) -> None:
        self._connected = False
        self._closed = True

    def send(self, message: str, *, timeout_seconds: float = 60.0) -> None:
        """Send one complete message to X4 (blocking until the write is done)."""
        if timeout_seconds <= 0:
            raise ValueError("send timeout must be positive")
        if not self._connected:
            raise TransportDisconnectedError("no client connected")
        req = _Request("send", message)
        self._queue.put(req)
        if not req.done.wait(timeout_seconds):
            raise TransportDisconnectedError("write timed out")
        if req.error is not None:
            raise TransportDisconnectedError(f"write failed: {req.error}")

    def recv(self, timeout_seconds: float) -> str | None:
        """Get the next message from X4, or None if none within *timeout_seconds*.

        Raises ``TransportDisconnectedError`` if the peer closed the pipe."""
        if not self._connected:
            raise TransportDisconnectedError("no client connected")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        req = _Request("recv", timeout_seconds=timeout_seconds)
        self._queue.put(req)
        if not req.done.wait(timeout_seconds + 1.0):
            raise TransportDisconnectedError("read worker did not finish")
        if req.error is not None:
            raise TransportDisconnectedError(str(req.error))
        if req.timed_out:
            return None
        if req.result is None:
            # Empty read / EOF.
            raise TransportDisconnectedError("peer closed the pipe")
        return req.result

    def close(self) -> None:
        """Close the connection idempotently."""
        if self._file is None:
            self._closed = True
            self._connected = False
            return
        self._closed = True
        self._connected = False
        # Ask the I/O thread to stop and let it close the handle (it is the
        # sole owner of the handle, so closing from this thread would race it).
        self._queue.put(_SHUTDOWN)
        if self._io_thread is not None:
            self._io_thread.join(timeout=1.0)
        # Best-effort: if the I/O thread never got to close (e.g. it is still
        # blocked on a ReadFile), drop our reference.  The OS frees the pipe
        # when the owning process/thread ends; we never reuse this handle.
        if self._file is not None:
            self._file = None

    def is_connected(self) -> bool:
        return self._connected and self._file is not None

