"""Telegram client lifecycle and local session locking."""

import os
from pathlib import Path
from functools import wraps
from typing import Optional

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.prompt import Prompt

from telegram_toolkit.utils.config import get_credentials

console = Console()


def _lock_path(session_name: str) -> Path:
    return Path(f"{session_name}.toolkit.lock")


def _pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _acquire_lock(session_name: str) -> Path:
    """Prevent two toolkit processes from opening the same session at once."""
    path = _lock_path(session_name)
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
        return path
    except FileExistsError:
        try:
            pid = int(path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            pid = -1
        if pid > 0 and _pid_is_running(pid):
            raise RuntimeError(
                f"Another Telegram Toolkit process is already using this session (PID {pid}). "
                "Close it before starting another command."
            )
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
        return path


def _release_lock(path: Optional[Path]) -> None:
    if path is None:
        return
    try:
        path.unlink()
    except (FileNotFoundError, OSError):
        pass


def _patch_disconnect(client: TelegramClient, lock_path: Path) -> TelegramClient:
    """Release the process lock whenever the client disconnects."""
    original_disconnect = client.disconnect

    @wraps(original_disconnect)
    def disconnect_and_unlock(*args, **kwargs):
        try:
            return original_disconnect(*args, **kwargs)
        finally:
            _release_lock(lock_path)

    client.disconnect = disconnect_and_unlock
    return client


def get_telegram_client():
    """Create an authorized Telegram client and preserve its session cache."""
    credentials = get_credentials()
    if not credentials:
        return None

    api_id, api_hash, phone = credentials
    session_name = f"telegram_toolkit_{phone.replace('+', '').replace(' ', '')}"
    lock_path = None

    try:
        lock_path = _acquire_lock(session_name)
        console.print("[green]Connecting to Telegram...[/green]")
        client = TelegramClient(session_name, int(api_id), api_hash)
        client.connect()

        if not client.is_user_authorized():
            console.print("[yellow]Authorization required.[/yellow]")
            client.send_code_request(phone)
            code = Prompt.ask("[bold green]Enter the code you received")
            try:
                client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = Prompt.ask(
                    "[bold yellow]Two-step verification enabled. Enter your password",
                    password=True,
                )
                client.sign_in(password=password)

        client = _patch_disconnect(client, lock_path)
        lock_path = None
        console.print("[bold green]Successfully connected to Telegram![/bold green]")
        return client

    except Exception as e:
        _release_lock(lock_path)
        console.print(f"[bold red]Error connecting to Telegram: {str(e)}[/bold red]")
        if "database is locked" in str(e).lower():
            console.print(
                "[yellow]The Telegram session database is locked. "
                "Make sure no other Telegram Toolkit/Telethon process is using this session.[/yellow]"
            )
        return None
