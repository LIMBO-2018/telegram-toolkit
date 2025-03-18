"""
Telegram client utilities.
"""

import os
import time
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.prompt import Prompt
from configparser import ConfigParser
from dotenv import load_dotenv

console = Console()

def get_telegram_client():
    """Get a Telegram client instance."""
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = ConfigParser()
    if not os.path.exists('config.data'):
        console.print("[bold red]Configuration not found. Run 'telegram-toolkit setup --config' first.[/bold red]")
        return None
    
    config.read('config.data')
    
    # Get credentials
    try:
        api_id = config['cred']['id']
        api_hash = config['cred']['hash']
        phone = config['cred']['phone']
    except KeyError:
        console.print("[bold red]Invalid configuration. Run 'telegram-toolkit setup --config' again.[/bold red]")
        return None
    
    # Generate a unique session name based on phone number
    session_name = f"telegram_toolkit_{phone.replace('+', '')}"
    
    # Remove existing session files if they exist and seem to be locked
    if os.path.exists(f"{session_name}.session"):
        if os.path.exists(f"{session_name}.session-journal"):
            console.print("[yellow]Cleaning up previous session files...[/yellow]")
            try:
                os.remove(f"{session_name}.session")
                os.remove(f"{session_name}.session-journal")
                time.sleep(1)  # Give the OS time to release the files
            except Exception as e:
                console.print(f"[yellow]Warning: Could not remove session files: {e}[/yellow]")
    
    # Create the client
    try:
        console.print("[green]Connecting to Telegram...[/green]")
        client = TelegramClient(session_name, api_id, api_hash)
        client.connect()
        
        # Check if already authorized
        if not client.is_user_authorized():
            console.print("[yellow]Authorization required.[/yellow]")
            client.send_code_request(phone)
            code = Prompt.ask("[bold green]Enter the code you received")
            
            try:
                client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = Prompt.ask("[bold yellow]Two-step verification enabled. Enter your password", password=True)
                client.sign_in(password=password)
        
        console.print("[bold green]Successfully connected to Telegram![/bold green]")
        return client
    
    except Exception as e:
        console.print(f"[bold red]Error connecting to Telegram: {str(e)}[/bold red]")
        if "database is locked" in str(e):
            console.print("[yellow]The session database is locked. This might be due to another instance running.[/yellow]")
            console.print("[yellow]Try removing the session files manually and run the command again.[/yellow]")
        return None
