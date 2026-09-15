"""Validated CSV handling utilities."""

import csv
from pathlib import Path

from rich.console import Console

console = Console()
CSV_FIELDS = ["id", "access_hash", "username", "name", "group"]


def save_members_to_csv(members, group, output_file):
    """Save Telegram member records to a UTF-8 CSV file."""
    output = Path(output_file)
    try:
        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for member in members:
                writer.writerow({
                    "id": getattr(member, "id", ""),
                    "access_hash": getattr(member, "access_hash", ""),
                    "username": getattr(member, "username", "") or "",
                    "name": " ".join(filter(None, [getattr(member, "first_name", ""), getattr(member, "last_name", "")])),
                    "group": getattr(group, "title", ""),
                })
        console.print(f"[bold green]Members saved to {output}[/bold green]")
        return True
    except (OSError, csv.Error) as exc:
        console.print(f"[bold red]Error saving members to CSV: {exc}[/bold red]")
        return False


def load_members_from_csv(input_file):
    """Load and validate member records from a CSV file."""
    members = []
    required = set(CSV_FIELDS)
    try:
        with Path(input_file).open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                missing = ", ".join(sorted(required - set(reader.fieldnames or [])))
                raise ValueError(f"Invalid CSV header; missing: {missing}")

            for line_number, row in enumerate(reader, start=2):
                try:
                    user_id = int((row.get("id") or "").strip())
                    access_hash = int((row.get("access_hash") or "").strip())
                    if not user_id or not access_hash:
                        raise ValueError("id/access_hash cannot be zero")
                    members.append({
                        "id": user_id,
                        "access_hash": access_hash,
                        "username": (row.get("username") or "").strip(),
                        "name": (row.get("name") or "").strip(),
                        "group": (row.get("group") or "").strip(),
                    })
                except (TypeError, ValueError) as exc:
                    console.print(f"[yellow]Skipping invalid CSV row {line_number}: {exc}[/yellow]")

        console.print(f"[bold green]Loaded {len(members)} valid members from {input_file}[/bold green]")
        return members
    except (OSError, csv.Error, ValueError) as exc:
        console.print(f"[bold red]Error loading members from CSV: {exc}[/bold red]")
        return []


def merge_csv_files(file1, file2, output_file="merged.csv"):
    """Merge two member CSVs, deduplicating by Telegram user ID."""
    members1 = load_members_from_csv(file1)
    members2 = load_members_from_csv(file2)
    merged = {}
    conflicts = 0

    for member in members1 + members2:
        existing = merged.get(member["id"])
        if existing is None:
            merged[member["id"]] = member
        elif existing["access_hash"] != member["access_hash"]:
            conflicts += 1
            # Access hashes are account/session-specific; do not silently replace
            # a previously loaded value when two sources disagree.

    if conflicts:
        console.print(
            f"[bold yellow]Warning: {conflicts} duplicate IDs had different access hashes. "
            "The first record was retained.[/bold yellow]"
        )

    try:
        with Path(output_file).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(merged.values())
        console.print(f"[bold green]Merged {len(merged)} unique members to {output_file}[/bold green]")
        return True
    except (OSError, csv.Error) as exc:
        console.print(f"[bold red]Error merging CSV files: {exc}[/bold red]")
        return False
