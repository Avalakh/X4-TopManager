"""Require the same Windows account as the running X4 process."""

from __future__ import annotations

import ctypes
import os


def current_account() -> str:
    if os.name != "nt":
        raise RuntimeError("TopManager runtime requires Windows")
    size = ctypes.c_ulong(256)
    name = ctypes.create_unicode_buffer(size.value)
    if not ctypes.windll.secur32.GetUserNameExW(2, name, ctypes.byref(size)):
        raise RuntimeError("Cannot verify the Windows process account")
    return name.value.casefold()


def require_avalakh() -> None:
    """Legacy call name; verify the runtime user against live X4 when present."""
    account = current_account()
    owners = running_x4_accounts()
    if owners and account not in owners:
        raise RuntimeError(
            f"TopManager refused to start under {account}; running X4 belongs to {', '.join(sorted(owners))}"
        )


def running_x4_accounts() -> set[str]:
    """Read process owners without relying on a machine-specific account name."""
    if os.name != "nt":
        raise RuntimeError("TopManager runtime requires Windows")
    import win32api
    import win32con
    import win32security
    import csv
    import subprocess

    owners: set[str] = set()
    listing = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq X4.exe', '/FO', 'CSV', '/NH'],
                             capture_output=True, text=True, timeout=10,
                             creationflags=subprocess.CREATE_NO_WINDOW, check=True)
    for row in csv.reader(listing.stdout.splitlines()):
        if len(row) >= 2 and row[0].casefold() == 'x4.exe':
            process = win32api.OpenProcess(0x1000, False, int(row[1]))
            token = win32security.OpenProcessToken(process, win32con.TOKEN_QUERY)
            try:
                sid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
                user, domain, _ = win32security.LookupAccountSid(None, sid)
                owners.add(f"{domain}\\{user}".casefold())
            finally:
                token.Close()
                process.Close()
    return owners
