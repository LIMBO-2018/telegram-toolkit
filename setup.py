#!/usr/bin/env python3
"""
Setup script for Telegram Toolkit.
"""

from setuptools import setup, find_packages
import os

# Define requirements directly
requirements = [
    'telethon>=1.24.0',
    'rich>=10.0.0',
    'typer>=0.4.0',
    'configparser>=5.0.0',
    'python-dotenv>=0.19.0',
    'tqdm>=4.64.0',
    'pyfiglet>=0.8.post1',
]

# Read README for long description if it exists
long_description = "A professional tool for Telegram group management and member scraping"
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="telegram-toolkit",
    version="1.0.0",
    description="A professional tool for Telegram group management and member scraping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/telegram-toolkit",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'telegram-toolkit=telegram_toolkit.__main__:app',
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

