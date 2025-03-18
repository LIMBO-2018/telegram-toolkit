#!/usr/bin/env python3
"""
Example script to scrape members from one group and add them to another.
"""

import subprocess
import time
import os

# Configuration
SOURCE_GROUP_NAME = "Source Group"  # Name of the group to scrape from
TARGET_GROUP_NAME = "Target Group"  # Name of the group to add members to
DELAY_BETWEEN_ADDS = 15  # Delay in seconds between adding members
MAX_MEMBERS_TO_ADD = 50  # Maximum number of members to add (0 for all)
OUTPUT_FILE = "members.csv"  # File to save scraped members

def main():
    """Main function."""
    print(f"Starting automated scrape and add process...")
    
    # Scrape members
    print(f"Scraping members from '{SOURCE_GROUP_NAME}'...")
    subprocess.run(["telegram-toolkit", "scrape", "--output", OUTPUT_FILE])
    
    # Wait a bit
    print("Waiting 5 seconds before adding members...")
    time.sleep(5)
    
    # Add members
    print(f"Adding members to '{TARGET_GROUP_NAME}'...")
    cmd = ["telegram-toolkit", "add", OUTPUT_FILE, "--delay", str(DELAY_BETWEEN_ADDS)]
    if MAX_MEMBERS_TO_ADD > 0:
        cmd.extend(["--limit", str(MAX_MEMBERS_TO_ADD)])
    subprocess.run(cmd)
    
    print("Process completed!")

if __name__ == "__main__":
    main()
