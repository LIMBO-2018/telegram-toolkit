"""
Utilities for working with CSV files.
"""

from telegram_toolkit.utils.csv_handler import merge_csv_files as merge_csv

def merge_csv_files(file1, file2, output_file="merged.csv"):
    """Merge two CSV files with members."""
    merge_csv(file1, file2, output_file)
