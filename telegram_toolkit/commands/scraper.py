"""
Member scraping functionality.
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from rich.console import Console
from rich.prompt import IntPrompt
from rich.progress import Progress
import time
from datetime import datetime, timedelta

from telegram_toolkit.utils.client import get_telegram_client
from telegram_toolkit.utils.csv_handler import save_members_to_csv

console = Console()

def scrape_members(output_file="members.csv", filter_active=False, limit=0):
    """Scrape members from a Telegram group."""
    client = get_telegram_client()
    if not client:
        return
    
    try:
        # Get all dialogs
        console.print("[bold yellow]Fetching dialogs...[/bold yellow]")
        
        with Progress() as progress:
            task = progress.add_task("[green]Fetching dialogs...", total=None)
            
            result = client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))
            
            progress.update(task, completed=True)
        
        # Filter for groups
        groups = []
        for chat in result.chats:
            if hasattr(chat, 'megagroup') and chat.megagroup:
                groups.append(chat)
        
        # Display groups
        console.print("[bold green]Available Groups:[/bold green]")
        for i, group in enumerate(groups):
            console.print(f"[cyan]{i}[/cyan]: [yellow]{group.title}[/yellow] (ID: {group.id})")
        
        # Select group
        group_index = IntPrompt.ask(
            "[bold green]Enter the number of the group to scrape",
            default=0,
            show_default=True
        )
        
        if group_index < 0 or group_index >= len(groups):
            console.print("[bold red]Invalid group selection.[/bold red]")
            return
        
        target_group = groups[group_index]
        console.print(f"[bold green]Selected group: [yellow]{target_group.title}[/yellow][/bold green]")
        
        # Fetch members
        console.print("[bold yellow]Fetching members...[/bold yellow]")
        
        with Progress() as progress:
            task = progress.add_task("[green]Fetching members...", total=None)
            
            all_members = []
            
            # Get all participants with a limit if specified
            participants = client.get_participants(
                target_group,
                aggressive=True,
                limit=limit if limit > 0 else None
            )
            
            # Filter active users if requested
            if filter_active:
                now = datetime.now()
                one_week_ago = now - timedelta(days=7)
                
                for participant in participants:
                    if hasattr(participant.status, 'was_online') and participant.status.was_online:
                        last_seen = participant.status.was_online
                        if last_seen > one_week_ago:
                            all_members.append(participant)
            else:
                all_members = participants
            
            progress.update(task, completed=True)
        
        # Save to CSV
        console.print(f"[bold green]Found {len(all_members)} members.[/bold green]")
        save_members_to_csv(all_members, target_group, output_file)
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
    finally:
        client.disconnect()
