"""
Add members to a Telegram group.
"""

import time
import random
from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.progress import Progress
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError, FloodWaitError, UserNotMutualContactError, UserChannelsTooMuchError

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import load_members_from_csv

console = Console()

def add_members(input_file, delay=15, limit=0):
    """Add members to a Telegram group."""
    client = get_telegram_client()
    if not client:
        return
    
    try:
        # Load members from CSV
        members = load_members_from_csv(input_file)
        
        # Get available groups
        dialogs = client.get_dialogs()
        groups = []
        
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                groups.append(dialog)
        
        if not groups:
            console.print("[bold red]No groups found.[/bold red]")
            return
        
        # Display available groups with proper indexing
        for i, dialog in enumerate(groups):
            console.print(f"[cyan]{i+1}[/cyan]: {dialog.name}")
        
        # Select target group
        group_index = IntPrompt.ask(
            "[bold green]Select a group to add members to",
            default=1,
            show_default=True
        ) - 1
        
        if group_index < 0 or group_index >= len(groups):
            console.print("[bold red]Invalid group selection. Please choose a number between 1 and " + str(len(groups)) + ".[/bold red]")
            return
        
        target_group = groups[group_index]
        
        # Ask for mode
        console.print("[bold green]Select mode:[/bold green]")
        console.print("[cyan]1[/cyan]: Add by user ID")
        console.print("[cyan]2[/cyan]: Add by username")
        
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
            f"[bold yellow]You are about to add {total_members} members to {target_group.name} chat. Continue?[/bold yellow]",
            choices=["y", "n"],
            default="n"
        )
        
        if confirm.lower() != "y":
            console.print("[bold yellow]Operation cancelled.[/bold yellow]")
            return
        
        # Add members
        added = 0
        errors = 0
        
        with Progress() as progress:
            task = progress.add_task("[green]Adding members...", total=total_members)
            
            for i, user in enumerate(members):
                if limit > 0 and added >= limit:
                    break
                
                try:
                    if mode == 1:
                        user_to_add = client.get_input_entity(int(user['id']))
                    else:
                        if not user['username']:
                            console.print(f"[yellow]Skipping user {user['name']} (no username)[/yellow]")
                            continue
                        user_to_add = client.get_input_entity(user['username'])
                    
                    client(InviteToChannelRequest(
                        channel=target_group.id,
                        users=[user_to_add]
                    ))
                    
                    added += 1
                    console.print(f"[green]Added {user['name']} ({added}/{total_members})[/green]")
                    
                    # Random delay to avoid flood
                    actual_delay = delay + random.randint(-5, 5)
                    if actual_delay < 5:
                        actual_delay = 5
                    
                    time.sleep(actual_delay)
                    
                except UserPrivacyRestrictedError:
                    console.print(f"[yellow]Couldn't add {user['name']} due to privacy settings.[/yellow]")
                    errors += 1
                except FloodWaitError as e:
                    wait_time = e.seconds
                    console.print(f"[bold red]Flood wait error. Waiting for {wait_time} seconds.[/bold red]")
                    time.sleep(wait_time)
                except UserNotMutualContactError:
                    console.print(f"[yellow]Couldn't add {user['name']} because they don't have you as a contact.[/yellow]")
                    errors += 1
                except UserChannelsTooMuchError:
                    console.print(f"[yellow]Couldn't add {user['name']} because they're in too many channels.[/yellow]")
                    errors += 1
                except Exception as e:
                    console.print(f"[red]Error adding {user['name']}: {str(e)}[/red]")
                    errors += 1
                
                progress.update(task, advance=1)
        
        console.print(f"[bold green]Added {added} members successfully.[/bold green]")
        if errors > 0:
            console.print(f"[bold yellow]Encountered {errors} errors.[/bold yellow]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        client.disconnect()
