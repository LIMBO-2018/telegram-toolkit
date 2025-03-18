"""
Configuration utilities for Telegram Toolkit.
"""

import os
import configparser
from rich.console import Console
from rich.prompt import Prompt
import dotenv
from pathlib import Path

console = Console()

CONFIG_FILE = "config.data"
ENV_FILE = ".env"

def check_config_exists():
    """Check if the configuration file exists."""
    return os.path.exists(CONFIG_FILE)

def load_config():
    """Load configuration from config file."""
    if not check_config_exists():
        console.print("[bold red]Configuration file not found. Run setup first.[/bold red]")
        return None
    
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_config(api_id, api_hash, phone):
    """Save API configuration to config file."""
    config = configparser.RawConfigParser()
    config.add_section('cred')
    config.set('cred', 'id', api_id)
    config.set('cred', 'hash', api_hash)
    config.set('cred', 'phone', phone)
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    # Also save to .env for alternative configuration
    with open(ENV_FILE, 'w') as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"PHONE={phone}\n")
    
    console.print("[bold green]Configuration saved successfully![/bold green]")

def get_credentials():
    """Get API credentials from config file."""
    if os.path.exists(ENV_FILE):
        dotenv.load_dotenv(ENV_FILE)
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        phone = os.getenv("PHONE")
        if api_id and api_hash and phone:
            return api_id, api_hash, phone
    
    config = load_config()
    if not config:
        return None, None, None
    
    try:
        api_id = config['cred']['id']
        api_hash = config['cred']['hash']
        phone = config['cred']['phone']
        return api_id, api_hash, phone
    except KeyError:
        console.print("[bold red]Invalid configuration file. Run setup again.[/bold red]")
        return None, None, None
