"""Transport abstraction for the Named Pipe channel (tasks 1.4-1.6).

``Transport`` is the replaceable edge of the protocol. All protocol objects
(``Message``, ``MessageCodec``) are transport-agnostic; they never import or
reference a concrete transport (design.md §6.1).

Contract:
  * one ``send`` == one complete message (the transport owns message framing);
  * one ``recv`` == one complete message, or ``None`` within the timeout window;
  * ``recv`` must be interruptible by timeout;
  * the transport never mutates the protocol payload; it only moves text.

Concrete transports: ``InMemoryPipe`` (fake, for tests/smoke) and
``NamedPipeTransport`` (real Windows named pipe, lazy pywin32 import).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"


class TransportError(RuntimeError):
    """Base runtime error for a transport."""


class TransportDisconnectedError(TransportError):
    """The peer closed the connection or the pipe is no longer open."""


class MessageTransportError(TransportError):
    """A malformed/unexpected message arrived on the wire."""


class Transport(ABC):
    """Replaceable message transport."""

    @abstractmethod
    def connect(self) -> None:
        """Establish the connection. Idempotent; raises on failure."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send one complete message (UTF-8 text). Blocking, but not on the
        game frame loop; this is a short-lived pipe write."""

    @abstractmethod
    def recv(self, timeout_seconds: float) -> str | None:
        """Return the next complete message, or None if none arrives within
        *timeout_seconds*. Raises TransportDisconnectedError if the peer closed."""

    @abstractmethod
    def close(self) -> None:
        """Close the connection idempotently."""

    @abstractmethod
    def is_connected(self) -> bool:
        """True while a peer is connected and usable."""

    @property
    def state(self) -> ConnectionState:
        """Current connection state."""
        if self.is_connected():
            return ConnectionState.CONNECTED
        return ConnectionState.DISCONNECTED
