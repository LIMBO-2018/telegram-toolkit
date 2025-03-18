"""
Send messages to Telegram users.
"""

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.progress import Progress
import time
import random

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import load_members_from_csv

console = Console()

def send_messages(input_file, message, delay=30, limit=0):
    """Send messages to Telegram users."""
    client = get_telegram_client()
    if not client:
        return
    
    try:
        # Load members from CSV
        members = load_members_from_csv(input_file)
        
        # Ask for mode
        console.print("[bold green]Select mode:[/bold green]")
        console.print("[cyan]1[/cyan]: Send by user ID")
        console.print("[cyan]2[/cyan]: Send by username")
        
        mode = IntPrompt.ask(
            "[bold green]Enter mode",
            default=1,
            show_default=True
        )
        
        if mode not in [1, 2]:
            console.print("[bold red]Invalid mode selection.[/bold red]")
            return
        
        # Confirm before proceeding
        total_members = len(members)
        if limit > 0 and limit < total_members:
            total_members = limit
        
        confirm = Prompt.ask(
            f"[bold yellow]You are about to send messages to {total_members} users. Continue?[/bold yellow]",
            choices=["y", "n"],
            default="n"
        )
        
        if confirm.lower() != "y":
            console.print("[bold yellow]Operation cancelled.[/bold yellow]")
            return
        
        # Send messages
        sent = 0
        errors = 0
        
        with Progress() as progress:
            task = progress.add_task("[green]Sending messages...", total=total_members)
            
            for i, user in enumerate(members):
                if limit > 0 and sent >= limit:
                    break
                
                try:
                    if mode == 1:
                        receiver = InputPeerUser(user['id'], user['access_hash'])
                    else:
                        if not user['username']:
                            console.print(f"[yellow]Skipping user {user['name']} (no username)[/yellow]")
                            continue
                        receiver = client.get_input_entity(user['username'])
                    
                    # Format message with user's name
                    formatted_message = message.format(name=user['name'])
                    
                    client.send_message(receiver, formatted_message)
                    
                    sent += 1
                    console.print(f"[green]Message sent to {user['name']} ({sent}/{total_members})[/green]")
                    
                    # Random delay to avoid flood
                    actual_delay = delay + random.randint(-5, 5)
                    if actual_delay < 5:
                        actual_delay = 5
                    
                    time.sleep(actual_delay)
                    
                except PeerFloodError:
                    console.print("[bold red]Telegram is limiting your requests. Try again later.[/bold red]")
                    break
                except UserPrivacyRestrictedError:
                    console.print(f"[yellow]Couldn't message {user['name']} due to privacy settings.[/yellow]")
                    errors += 1
                except Exception as e:
                    console.print(f"[red]Error messaging {user['name']}: {str(e)}[/red]")
                    errors += 1
                
                progress.update(task, advance=1)
        
        console.print(f"[bold green]Sent {sent} messages successfully.[/bold green]")
        if errors > 0:
            console.print(f"[bold yellow]Encountered {errors} errors.[/bold yellow]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        client.disconnect()
