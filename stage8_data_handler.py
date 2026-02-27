"""
WEEK 8 - File Handling: CSV + JSON + Pandas
Stores, Reads, and Syncs data across multiple file structures
"""

import json
import csv
import pandas as pd

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[{filename}] Saved JSON data")

def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def export_to_csv(data, filename):
    if not data:
        print("No data to export.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"[{filename}] Exported to CSV")

def review_with_pandas(filename):
    try:
        df = pd.read_csv(filename)
        print("\n--- Pandas DataFrame View ---")
        print(df)
        print("\n--- Aggregation (Counts by Category) ---")
        print(df['category'].value_counts())
    except FileNotFoundError:
        print(f"[{filename}] File not found.")
    except Exception as e:
        print(f"Pandas Error: {e}")

if __name__ == "__main__":
    sample_records = [
        {"id": 1, "student_name": "Nivas", "category": "Hostel", "status": "Pending"},
        {"id": 2, "student_name": "Alice", "category": "Academic", "status": "Resolved"},
        {"id": 3, "student_name": "Bob", "category": "Academic", "status": "In Progress"}
    ]
    
    # Simulating data persistence execution
    save_to_json(sample_records, 'temp_grievances.json')
    loaded_data = load_from_json('temp_grievances.json')
    
    export_to_csv(loaded_data, 'temp_grievances.csv')
    review_with_pandas('temp_grievances.csv')
