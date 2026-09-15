"""Consent-based Telegram messaging with explicit flood-limit handling."""

from rich.console import Console
from rich.progress import Progress
from rich.prompt import IntPrompt, Prompt
from telethon.errors.rpcerrorlist import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.types import InputPeerUser

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import load_members_from_csv

console = Console()


def send_messages(input_file, message, delay=30, limit=0):
    """Send a message only to an explicitly authorized recipient list."""
    if delay < 0 or limit < 0:
        console.print("[bold red]Delay and limit must be zero or greater.[/bold red]")
        return False

    client = get_telegram_client()
    if not client:
        return False

    try:
        members = load_members_from_csv(input_file)
        if not members:
            console.print("[bold red]No valid recipients found in the CSV.[/bold red]")
            return False

        console.print("[bold green]Select mode:[/bold green]")
        console.print("[cyan]1[/cyan]: Send by CSV user ID + access hash")
        console.print("[cyan]2[/cyan]: Resolve by username")
        mode = IntPrompt.ask("[bold green]Enter mode[/bold green]", default=1)
        if mode not in (1, 2):
            console.print("[bold red]Invalid mode selection.[/bold red]")
            return False

        selected = members[:limit] if limit > 0 else members
        console.print(
            f"[bold yellow]Only message recipients who have explicitly opted in. "
            f"Recipients: {len(selected)}.[/bold yellow]"
        )
        confirm = Prompt.ask("Continue?", choices=["y", "n"], default="n")
        if confirm.lower() != "y":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return False

        sent = 0
        errors = 0
        with Progress() as progress:
            task = progress.add_task("[green]Sending messages...", total=len(selected))
            for user in selected:
                try:
                    if mode == 1:
                        receiver = InputPeerUser(int(user["id"]), int(user["access_hash"]))
                    else:
                        username = (user.get("username") or "").strip()
                        if not username:
                            raise ValueError("no username available")
                        receiver = client.get_input_entity(username)

                    formatted_message = message.format(name=user.get("name", ""))
                    client.send_message(receiver, formatted_message)
                    sent += 1
                    console.print(f"[green]Message sent to {user['name']} ({sent}/{len(selected)})[/green]")
                except FloodWaitError as exc:
                    console.print(
                        f"[bold red]Telegram requested a flood wait of {exc.seconds} seconds. "
                        "Stopping safely instead of bypassing the limit.[/bold red]"
                    )
                    errors += 1
                    break
                except PeerFloodError:
                    console.print("[bold red]Telegram has limited messaging for this account. Stopping safely.[/bold red]")
                    errors += 1
                    break
                except UserPrivacyRestrictedError:
                    console.print(f"[yellow]Privacy settings prevent messaging {user['name']}.[/yellow]")
                    errors += 1
                except Exception as exc:
                    console.print(f"[red]Error messaging {user['name']}: {exc}[/red]")
                    errors += 1
                finally:
                    progress.advance(task)

        console.print(f"[bold green]Sent {sent} messages successfully.[/bold green]")
        if errors:
            console.print(f"[bold yellow]Encountered {errors} errors.[/bold yellow]")
        return errors == 0
    finally:
        client.disconnect()
