"""Configuration utilities for Telegram Toolkit."""

import configparser
import os
from pathlib import Path

import dotenv
from rich.console import Console

console = Console()

CONFIG_FILE = Path("config.data")
ENV_FILE = Path(".env")


def _valid_credentials(api_id, api_hash, phone):
    """Return True only when all required credentials are present and usable."""
    if not api_id or not api_hash or not phone:
        return False
    try:
        int(str(api_id).strip())
    except (TypeError, ValueError):
        return False
    return bool(str(api_hash).strip() and str(phone).strip())


def check_config_exists():
    """Check whether usable Telegram credentials are configured."""
    credentials = get_credentials(silent=True)
    return bool(credentials)


def load_config():
    """Load the legacy config.data file."""
    if not CONFIG_FILE.exists():
        return None
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    return config


def save_config(api_id, api_hash, phone):
    """Validate and save Telegram API credentials to local config files."""
    api_id = str(api_id).strip()
    api_hash = str(api_hash).strip()
    phone = str(phone).strip()
    if not _valid_credentials(api_id, api_hash, phone):
        raise ValueError("Invalid API ID, API Hash, or phone number.")

    config = configparser.ConfigParser()
    config["cred"] = {"id": api_id, "hash": api_hash, "phone": phone}
    CONFIG_FILE.write_text(_config_to_text(config), encoding="utf-8")
    ENV_FILE.write_text(
        f"API_ID={api_id}\nAPI_HASH={api_hash}\nPHONE={phone}\n",
        encoding="utf-8",
    )
    console.print("[bold green]Configuration saved successfully![/bold green]")


def _config_to_text(config):
    from io import StringIO
    buffer = StringIO()
    config.write(buffer)
    return buffer.getvalue()


def get_credentials(silent=False):
    """Load credentials, preferring .env and falling back to config.data."""
    dotenv_values = dotenv.dotenv_values(ENV_FILE) if ENV_FILE.exists() else {}
    api_id = dotenv_values.get("API_ID")
    api_hash = dotenv_values.get("API_HASH")
    phone = dotenv_values.get("PHONE")

    if _valid_credentials(api_id, api_hash, phone):
        return str(api_id).strip(), str(api_hash).strip(), str(phone).strip()

    config = load_config()
    if config and config.has_section("cred"):
        api_id = config.get("cred", "id", fallback=None)
        api_hash = config.get("cred", "hash", fallback=None)
        phone = config.get("cred", "phone", fallback=None)
        if _valid_credentials(api_id, api_hash, phone):
            return str(api_id).strip(), str(api_hash).strip(), str(phone).strip()

    if not silent:
        console.print("[bold red]Configuration not found or invalid. Run 'telegram-toolkit setup --config'.[/bold red]")
    return None
