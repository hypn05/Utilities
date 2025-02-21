#!/usr/bin/env python3
"""A utility script to display a list of files with their descriptions in a pretty table."""

import json
from pathlib import Path
from prettytable import PrettyTable

def display_files_with_descriptions():
    # Get the parent directory of the current script
    parent_dir = Path("/Users/abali/Utilities")
    
    # Create a pretty table with headers
    table = PrettyTable()
    table.field_names = ["File Name", "Description"]
    table.align = "l"  # Set left alignment for all columns
    
    # Load files and descriptions from JSON file
    try:
        with open(parent_dir / "description.json", 'r', encoding='utf-8') as f:
            files_data = json.load(f)
    except FileNotFoundError:
        files_data = []
        print("Warning: description.json not found")
    except json.JSONDecodeError:
        files_data = []
        print("Warning: Invalid JSON in description.json")
    
    # Add each file and description from JSON to table
    for file_data in files_data:
        file_name = file_data.get('name', '')
        description = file_data.get('description', 'No description')
        table.add_row([file_name, description])
    
    # Print the table
    print(table)

if __name__ == "__main__":
    display_files_with_descriptions()
