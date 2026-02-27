"""
WEEK 10 Deliverable
Demonstrating Python Packages and Imports
"""

# Importing from our custom package: stage10_grievance_system
from stage10_grievance_system import *

def main():
    print("--- Using Package Imports ---")
    
    # Using format_category imported from package's __init__.py
    nice_category = format_category("examination")
    print(f"Formatted Category: {nice_category}")
    
    # Using process_grievance from package's __init__.py
    process_grievance("Nivas", "There is a mistake in my term paper grading.")

if __name__ == "__main__":
    main()
