#!/usr/bin/env python3
"""Packaging configuration for Telegram Toolkit."""

from pathlib import Path
from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
README = BASE_DIR / "README.md"
long_description = README.read_text(encoding="utf-8") if README.exists() else "Telegram group management toolkit."

requirements = [
    "telethon>=1.24.0",
    "rich>=10.0.0",
    "typer>=0.4.0",
    "configparser>=5.0.0",
    "python-dotenv>=0.19.0",
    "tqdm>=4.64.0",
    "pyfiglet>=0.8.post1",
]

setup(
    name="telegram-toolkit",
    version="1.0.0",
    description="A CLI toolkit for Telegram group management and member discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LIMBO",
    url="https://github.com/LIMBO-2018/telegram-toolkit",
    packages=find_packages(),
    entry_points={"console_scripts": ["telegram-toolkit=telegram_toolkit.__main__:app"]},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
