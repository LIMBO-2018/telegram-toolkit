
"""
CSV handling utilities.
"""

import csv
import os
from rich.console import Console

console = Console()

def save_members_to_csv(members, group, output_file):
    """Save members to a CSV file."""
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['id', 'access_hash', 'username', 'name', 'group'])
            
            # Write members
            for member in members:
                username = member.username if member.username else ""
                name = f"{member.first_name} {member.last_name if member.last_name else ''}"
                writer.writerow([
                    member.id,
                    member.access_hash,
                    username,
                    name.strip(),
                    group.title
                ])
        
        console.print(f"[bold green]Members saved to {output_file}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving members to CSV: {str(e)}[/bold red]")

def load_members_from_csv(input_file):
    """Load members from a CSV file."""
    members = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                members.append({
                    'id': int(row['id']),
                    'access_hash': int(row['access_hash']),
                    'username': row['username'],
                    'name': row['name'],
                    'group': row['group']
                })
        
        console.print(f"[bold green]Loaded {len(members)} members from {input_file}[/bold green]")
        return members
    except Exception as e:
        console.print(f"[bold red]Error loading members from CSV: {str(e)}[/bold red]")
        return []

def merge_csv_files(file1, file2, output_file="merged.csv"):
    """Merge two CSV files."""
    try:
        # Load members from both files
        members1 = load_members_from_csv(file1)
        members2 = load_members_from_csv(file2)
        
        # Combine members and remove duplicates based on ID
        seen_ids = set()
        merged_members = []
        
        for member in members1 + members2:
            if member['id'] not in seen_ids:
                seen_ids.add(member['id'])
                merged_members.append(member)
        
        # Save merged members
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['id', 'access_hash', 'username', 'name', 'group'])
            
            # Write members
            for member in merged_members:
                writer.writerow([
                    member['id'],
                    member['access_hash'],
                    member['username'],
                    member['name'],
                    member['group']
                ])
        
        console.print(f"[bold green]Merged {len(merged_members)} members to {output_file}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error merging CSV files: {str(e)}[/bold red]")

