"""
Telegram client utilities.
"""

import os
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.prompt import Prompt
from configparser import ConfigParser
from dotenv import load_dotenv

console = Console()

def get_telegram_client():
    """Get a Telegram client instance while preserving the Telethon session cache."""
    load_dotenv()

    config = ConfigParser()
    if not os.path.exists('config.data'):
        console.print("[bold red]Configuration not found. Run 'telegram-toolkit setup --config' first.[/bold red]")
        return None

    config.read('config.data')

    try:
        api_id = config['cred']['id']
        api_hash = config['cred']['hash']
        phone = config['cred']['phone']
    except KeyError:
        console.print("[bold red]Invalid configuration. Run 'telegram-toolkit setup --config' again.[/bold red]")
        return None

    session_name = f"telegram_toolkit_{phone.replace('+', '')}"

    try:
        console.print("[green]Connecting to Telegram...[/green]")
        # IMPORTANT: do not delete an existing .session file. Telethon uses it
        # to persist authorization and entity/access-hash information.
        client = TelegramClient(session_name, api_id, api_hash)
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
                    password=True
                )
                client.sign_in(password=password)

        console.print("[bold green]Successfully connected to Telegram![/bold green]")
        return client

    except Exception as e:
        console.print(f"[bold red]Error connecting to Telegram: {str(e)}[/bold red]")
        if "database is locked" in str(e):
            console.print("[yellow]The session database is locked. This might be due to another instance running.[/yellow]")
            console.print("[yellow]Close other Telegram-toolkit instances and try again.[/yellow]")
        return None
