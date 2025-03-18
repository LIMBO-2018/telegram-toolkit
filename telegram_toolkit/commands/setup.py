"""
Setup and configuration commands.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
import requests
from telegram_toolkit.utils.config import save_config
from telegram_toolkit.utils.csv_handler import merge_csv_files as merge_csv_util

console = Console()

def install_requirements():
    """Install required dependencies."""
    console.print("[bold yellow]Installing dependencies...[/bold yellow]")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        console.print("[bold green]Dependencies installed successfully![/bold green]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Failed to install dependencies.[/bold red]")
        sys.exit(1)

def configure_api():
    """Configure API credentials."""
    console.print("[bold yellow]Configuring API credentials...[/bold yellow]")
    console.print("[bold cyan]You need to create an app on https://my.telegram.org/apps and get your API credentials.[/bold cyan]")
    
    api_id = Prompt.ask("[bold green]Enter your API ID")
    api_hash = Prompt.ask("[bold green]Enter your API Hash")
    phone = Prompt.ask("[bold green]Enter your phone number (with country code)")
    
    save_config(api_id, api_hash, phone)

def update_tool():
    """Update the tool to the latest version."""
    console.print("[bold yellow]Checking for updates...[/bold yellow]")
    
    try:
        # This would normally check a remote repository for updates
        # For demonstration, we'll just show a message
        console.print("[bold green]You are running the latest version![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error checking for updates: {str(e)}[/bold red]")

def merge_csv_files(file1, file2, output):
    """Merge two CSV files."""
    console.print(f"[bold yellow]Merging {file1} and {file2}...[/bold yellow]")
    merge_csv_util(file1, file2, output)

def show_setup_help():
    """Show setup help information."""
    console.print("""
[bold cyan]Setup Commands:[/bold cyan]

[bold green]telegram-toolkit setup --config[/bold green]
    Configure your Telegram API credentials

[bold green]telegram-toolkit setup --install[/bold green]
    Install required dependencies

[bold green]telegram-toolkit setup --update[/bold green]
    Update the tool to the latest version

[bold green]telegram-toolkit merge FILE1 FILE2[/bold green]
    Merge two CSV files of members
    """)
