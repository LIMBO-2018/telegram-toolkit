"""Member discovery functionality."""

from datetime import datetime, timedelta, timezone

from rich.console import Console
from rich.prompt import IntPrompt
from rich.progress import Progress
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOnline, UserStatusOffline, UserStatusRecently

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import save_members_to_csv

console = Console()


def _is_active(user, cutoff):
    """Return whether Telegram exposes a recent enough status for this user."""
    status = getattr(user, "status", None)
    if isinstance(status, UserStatusOnline):
        return True
    if isinstance(status, UserStatusOffline):
        last_seen = status.was_online
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)
        return last_seen >= cutoff
    # Telegram's Recently status deliberately does not expose an exact time.
    # Treat it as active rather than inventing a timestamp.
    if isinstance(status, UserStatusRecently):
        return True
    return False


def _fetch_dialogs(client):
    """Fetch dialogs through Telethon's iterator so pagination is handled."""
    dialogs = []
    for dialog in client.iter_dialogs():
        dialogs.append(dialog)
    return dialogs


def scrape_members(output_file="members.csv", filter_active=False, limit=0):
    """Discover members from a group the logged-in account can access."""
    client = get_telegram_client()
    if not client:
        return False

    try:
        console.print("[bold yellow]Fetching dialogs...[/bold yellow]")
        dialogs = _fetch_dialogs(client)
        groups = [
            dialog.entity
            for dialog in dialogs
            if getattr(dialog, "is_group", False)
            and getattr(dialog.entity, "megagroup", False)
        ]

        if not groups:
            console.print("[bold red]No accessible groups found.[/bold red]")
            return False

        console.print("[bold green]Available Groups:[/bold green]")
        for i, group in enumerate(groups):
            console.print(f"[cyan]{i}[/cyan]: [yellow]{group.title}[/yellow] (ID: {group.id})")

        group_index = IntPrompt.ask(
            "[bold green]Enter the number of the group to inspect",
            default=0,
        )
        if not 0 <= group_index < len(groups):
            console.print("[bold red]Invalid group selection.[/bold red]")
            return False

        target_group = groups[group_index]
        console.print(f"[bold green]Selected group: [yellow]{target_group.title}[/yellow][/bold green]")
        console.print("[bold yellow]Fetching members...[/bold yellow]")

        fetch_limit = limit if limit > 0 else None
        participants = client.get_participants(target_group, limit=fetch_limit)

        if filter_active:
            cutoff = datetime.now(timezone.utc) - timedelta(days=7)
            members = [user for user in participants if _is_active(user, cutoff)]
        else:
            members = list(participants)

        console.print(f"[bold green]Found {len(members)} members.[/bold green]")
        save_members_to_csv(members, target_group, output_file)
        return True

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return False
    finally:
        client.disconnect()
