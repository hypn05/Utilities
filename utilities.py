#!/usr/bin/env python3
"""A utility script to display a list of files with their descriptions in a pretty table."""

from pathlib import Path
from prettytable import PrettyTable

def display_files_with_descriptions():
    # Get the parent directory of the current script
    parent_dir = Path("/Users/abali/Utilities")
    
    # Create a pretty table with headers
    table = PrettyTable()
    table.field_names = ["File Name", "Description"]
    table.align = "l"  # Set left alignment for all columns
    
    # Iterate through files in the parent directory
    for file_path in parent_dir.glob('*'):
        # Only process .py and bash files
        if file_path.is_file() and (file_path.suffix == '.py' or file_path.suffix == '.sh'):
            description = "No description"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Skip first line and read second line
                    f.readline()
                    second_line = f.readline().strip()
                    if second_line:
                        # Remove any comment characters and whitespace
                        description = second_line.lstrip('#').lstrip('/').strip().replace('"', '')
            except Exception as e:
                description = f"Error reading file: {str(e)}"
            
            # Add row to table
            table.add_row([file_path.name, description])
    
    # Print the table
    print(table)

if __name__ == "__main__":
    display_files_with_descriptions()
