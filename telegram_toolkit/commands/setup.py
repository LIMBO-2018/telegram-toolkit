"""Setup and configuration commands."""

import subprocess
import sys

from rich.console import Console
from rich.prompt import Prompt

from telegram_toolkit.utils.config import save_config
from telegram_toolkit.utils.csv_handler import merge_csv_files as merge_csv_util

console = Console()


def install_dependencies():
    """Install the dependencies declared by the project."""
    console.print("[bold yellow]Installing dependencies...[/bold yellow]")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as exc:
        console.print("[bold red]Failed to install dependencies.[/bold red]")
        return False
    console.print("[bold green]Dependencies installed successfully![/bold green]")
    return True


def configure_api():
    """Configure Telegram API credentials."""
    console.print("[bold cyan]Create an app at https://my.telegram.org/apps to obtain API credentials.[/bold cyan]")
    api_id = Prompt.ask("[bold green]Enter your API ID")
    api_hash = Prompt.ask("[bold green]Enter your API Hash")
    phone = Prompt.ask("[bold green]Enter your phone number (with country code)")
    save_config(api_id, api_hash, phone)


def update_tool():
    """Update the installed package from the current source checkout."""
    console.print("[bold yellow]Checking for updates...[/bold yellow]")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "."])
    except subprocess.CalledProcessError:
        console.print("[bold red]Update failed.[/bold red]")
        return False
    console.print("[bold green]Update completed successfully![/bold green]")
    return True


def merge_csv_files(file1, file2, output):
    """Merge two CSV files."""
    console.print(f"[bold yellow]Merging {file1} and {file2}...[/bold yellow]")
    return merge_csv_util(file1, file2, output)


def show_setup_help():
    """Show setup help information."""
    console.print("""
[bold cyan]Setup Commands:[/bold cyan]

[bold green]telegram-toolkit setup --config[/bold green]
    Configure Telegram API credentials

[bold green]telegram-toolkit setup --install[/bold green]
    Install project dependencies

[bold green]telegram-toolkit setup --update[/bold green]
    Update the local source installation

[bold green]telegram-toolkit merge FILE1 FILE2[/bold green]
    Merge two CSV files of members
""")
