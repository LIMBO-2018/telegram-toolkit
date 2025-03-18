#!/usr/bin/env python3
"""
Main entry point for the Telegram Toolkit.
"""

import os
import typer
from rich.console import Console
from rich import print
import pyfiglet

from telegram_toolkit.commands import setup, scraper, add_members, message_sender, csv_utils
from telegram_toolkit.utils.config import check_config_exists

app = typer.Typer()
console = Console()

def display_banner():
    """Display the application banner."""
    banner = pyfiglet.figlet_format("Telegram Toolkit", font="slant")
    console.print(f"[bold blue]{banner}[/bold blue]")
    console.print("[bold green]A professional tool for Telegram group management[/bold green]")
    console.print("[bold yellow]Use responsibly and respect Telegram's Terms of Service[/bold yellow]")
    console.print("")

@app.callback()
def callback():
    """
    Telegram Toolkit: A professional tool for Telegram group management.
    """
    display_banner()

@app.command("setup")
def setup_command(
    config: bool = typer.Option(False, "--config", "-c", help="Configure API credentials"),
    install: bool = typer.Option(False, "--install", "-i", help="Install dependencies"),
    update: bool = typer.Option(False, "--update", "-u", help="Update the tool")
):
    """Setup and configure the Telegram Toolkit."""
    if config:
        setup.configure()
    elif install:
        setup.install_dependencies()
    elif update:
        setup.update_tool()
    else:
        console.print("[bold yellow]Please specify an option: --config, --install, or --update[/bold yellow]")

@app.command("scrape")
def scrape_command(
    output: str = typer.Option("members.csv", "--output", "-o", help="Output file name"),
    active: bool = typer.Option(False, "--active", "-a", help="Only scrape active users"),
    limit: int = typer.Option(0, "--limit", "-l", help="Limit the number of members to scrape (0 for all)")
):
    """Scrape members from a Telegram group."""
    if not check_config_exists():
        console.print("[bold red]Configuration not found. Run 'telegram-toolkit setup --config' first.[/bold red]")
        return
    scraper.scrape_members(output, active, limit)

@app.command("add")
def add_command(
    input_file: str = typer.Argument(..., help="CSV file with members to add"),
    delay: int = typer.Option(10, "--delay", "-d", help="Delay between adding members (in seconds)"),
    limit: int = typer.Option(0, "--limit", "-l", help="Limit the number of members to add (0 for all)")
):
    """Add members to a Telegram group."""
    if not check_config_exists():
        console.print("[bold red]Configuration not found. Run 'telegram-toolkit setup --config' first.[/bold red]")
        return
    add_members.add_members(input_file, delay, limit)

@app.command("send")
def send_command(
    input_file: str = typer.Argument(..., help="CSV file with members to message"),
    message: str = typer.Option("Hello {name}, welcome to our group!", "--message", "-m", help="Message to send (can be a file path)"),
    delay: int = typer.Option(30, "--delay", "-d", help="Delay between sending messages (in seconds)"),
    limit: int = typer.Option(0, "--limit", "-l", help="Limit the number of messages to send (0 for all)")
):
    """Send messages to Telegram users."""
    if not check_config_exists():
        console.print("[bold red]Configuration not found. Run 'telegram-toolkit setup --config' first.[/bold red]")
        return
    
    # Check if message is a file path
    if os.path.isfile(message):
        with open(message, 'r', encoding='utf-8') as f:
            message_content = f.read()
    else:
        message_content = message
    
    message_sender.send_messages(input_file, message_content, delay, limit)

@app.command("merge")
def merge_command(
    file1: str = typer.Argument(..., help="First CSV file"),
    file2: str = typer.Argument(..., help="Second CSV file"),
    output: str = typer.Option("merged.csv", "--output", "-o", help="Output file name")
):
    """Merge two CSV files with members."""
    csv_utils.merge_csv_files(file1, file2, output)

if __name__ == "__main__":
    app()
