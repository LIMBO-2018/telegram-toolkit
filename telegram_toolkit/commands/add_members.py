"""Consent-based Telegram group member management."""

from rich.console import Console
from rich.progress import Progress
from rich.prompt import IntPrompt, Prompt
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    UserChannelsTooMuchError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import load_members_from_csv

console = Console()


def add_members(input_file, delay=15, limit=0):
    """Add explicitly authorized/consenting users from a CSV to a group."""
    if delay < 0 or limit < 0:
        console.print("[bold red]Delay and limit must be zero or greater.[/bold red]")
        return False

    client = get_telegram_client()
    if not client:
        return False

    try:
        members = load_members_from_csv(input_file)
        if not members:
            console.print("[bold red]No valid members found in the CSV.[/bold red]")
            return False

        dialogs = client.get_dialogs()
        groups = [dialog for dialog in dialogs if dialog.is_group or dialog.is_channel]
        if not groups:
            console.print("[bold red]No accessible groups found.[/bold red]")
            return False

        for i, dialog in enumerate(groups, start=1):
            console.print(f"[cyan]{i}[/cyan]: {dialog.name}")

        group_index = IntPrompt.ask("[bold green]Select a target group[/bold green]", default=1) - 1
        if not 0 <= group_index < len(groups):
            console.print("[bold red]Invalid group selection.[/bold red]")
            return False

        target_group = groups[group_index]
        selected = members[:limit] if limit > 0 else members
        console.print(
            f"[bold yellow]Only add users for whom you have appropriate consent/authorization. "
            f"Target: {target_group.name}; records: {len(selected)}.[/bold yellow]"
        )
        confirm = Prompt.ask("Continue?", choices=["y", "n"], default="n")
        if confirm.lower() != "y":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return False

        added = 0
        errors = 0
        with Progress() as progress:
            task = progress.add_task("[green]Adding members...", total=len(selected))
            for user in selected:
                try:
                    if not user.get("access_hash"):
                        raise ValueError("missing access_hash")
                    peer = InputPeerUser(int(user["id"]), int(user["access_hash"]))
                    client(InviteToChannelRequest(channel=target_group.entity, users=[peer]))
                    added += 1
                    console.print(f"[green]Added {user['name']} ({added}/{len(selected)})[/green]")
                except FloodWaitError as exc:
                    console.print(
                        f"[bold red]Telegram requested a flood wait of {exc.seconds} seconds. "
                        "Stopping safely instead of trying to bypass the limit.[/bold red]"
                    )
                    errors += 1
                    break
                except UserPrivacyRestrictedError:
                    console.print(f"[yellow]Privacy settings prevent adding {user['name']}.[/yellow]")
                    errors += 1
                except UserNotMutualContactError:
                    console.print(f"[yellow]Telegram requires a mutual contact for {user['name']}.[/yellow]")
                    errors += 1
                except UserChannelsTooMuchError:
                    console.print(f"[yellow]{user['name']} is in too many channels.[/yellow]")
                    errors += 1
                except Exception as exc:
                    console.print(f"[red]Error adding {user['name']}: {exc}[/red]")
                    errors += 1
                finally:
                    progress.advance(task)

        console.print(f"[bold green]Added {added} members successfully.[/bold green]")
        if errors:
            console.print(f"[bold yellow]Encountered {errors} errors.[/bold yellow]")
        return errors == 0
    finally:
        client.disconnect()
