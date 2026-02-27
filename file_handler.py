"""
File Handler Module
Handles all file operations for data persistence using JSON and CSV.
Demonstrates: File handling, JSON operations, CSV operations, error handling, exception handling
"""

import json
import csv
import os

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
GRIEVANCES_FILE = os.path.join(DATA_DIR, 'grievances.json')
GRIEVANCES_CSV = os.path.join(DATA_DIR, 'grievances.csv')

# CSV column headers
GRIEVANCE_CSV_HEADERS = [
    "id", "student_id", "student_name", "category",
    "description", "status", "response", "created_at",
    "updated_at", "resolved_at"
]


def initialize_data_files():
    """
    Create data directory and JSON/CSV files if they don't exist.
    Also creates a default admin account.
    
    Demonstrates: File handling, directory creation, error handling
    """
    # Create data directory
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print("[INFO] Created data directory.")
    
    # Initialize users.json with default admin
    if not os.path.exists(USERS_FILE):
        default_users = [
            {
                "id": 1,
                "name": "Admin",
                "email": "admin@college.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # '123456' hashed
                "role": "admin",
                "dept": "Administration",
                "created_at": "2026-01-24",
                "updated_at": ""
            }
        ]
        save_json(USERS_FILE, default_users)
        print("[INFO] Created users.json with default admin account.")
        print("       Default Admin: admin@college.com / 123456")
    
    # Initialize grievances.json
    if not os.path.exists(GRIEVANCES_FILE):
        save_json(GRIEVANCES_FILE, [])
        print("[INFO] Created grievances.json")
    
    # Initialize grievances.csv
    if not os.path.exists(GRIEVANCES_CSV):
        save_csv_headers(GRIEVANCES_CSV, GRIEVANCE_CSV_HEADERS)
        print("[INFO] Created grievances.csv")
    
    # Sync: ensure CSV has all data from JSON
    sync_json_to_csv()


# ==================== JSON OPERATIONS ====================

def load_json(filepath):
    """
    Load data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: Data loaded from file, or empty list if error
        
    Demonstrates: File reading, JSON parsing, exception handling
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"[WARNING] File not found: {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON in file: {filepath}")
        return []


def save_json(filepath, data):
    """
    Save data to a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        data (list): Data to save
        
    Returns:
        bool: True if successful, False otherwise
        
    Demonstrates: File writing, JSON serialization, exception handling
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Could not save JSON data: {e}")
        return False


# ==================== CSV OPERATIONS ====================

def save_csv_headers(filepath, headers):
    """
    Create a CSV file with headers only.
    
    Args:
        filepath (str): Path to the CSV file
        headers (list): Column header names
        
    Demonstrates: CSV file creation, file writing
    """
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    except Exception as e:
        print(f"[ERROR] Could not create CSV: {e}")


def load_csv(filepath):
    """
    Load data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        list: List of dictionaries (each row as dict)
        
    Demonstrates: CSV reading, DictReader usage
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                # Convert id fields to integers
                if 'id' in row and row['id']:
                    row['id'] = int(row['id'])
                if 'student_id' in row and row['student_id']:
                    row['student_id'] = int(row['student_id'])
                data.append(dict(row))
            return data
    except FileNotFoundError:
        print(f"[WARNING] CSV file not found: {filepath}")
        return []
    except Exception as e:
        print(f"[ERROR] Could not read CSV: {e}")
        return []


def save_csv(filepath, data, headers):
    """
    Save data to a CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        data (list): List of dictionaries to save
        headers (list): Column headers
        
    Returns:
        bool: True if successful, False otherwise
        
    Demonstrates: CSV writing, DictWriter usage
    """
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"[ERROR] Could not save CSV: {e}")
        return False


def append_csv(filepath, row_data, headers):
    """
    Append a single row to a CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        row_data (dict): Row data as dictionary
        headers (list): Column headers
        
    Returns:
        bool: True if successful
        
    Demonstrates: CSV append operation
    """
    try:
        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
            writer.writerow(row_data)
        return True
    except Exception as e:
        print(f"[ERROR] Could not append to CSV: {e}")
        return False


# ==================== SYNC OPERATIONS ====================

def sync_json_to_csv():
    """
    Synchronize grievances from JSON to CSV file.
    Ensures both storage formats have the same data.
    
    Demonstrates: Data synchronization, dual storage
    """
    grievances = load_json(GRIEVANCES_FILE)
    if grievances:
        save_csv(GRIEVANCES_CSV, grievances, GRIEVANCE_CSV_HEADERS)


# ==================== ID GENERATION ====================

def get_next_id(filepath):
    """
    Get the next available ID for a new record.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        int: Next available ID
        
    Demonstrates: Data iteration, max() function
    """
    data = load_json(filepath)
    if not data:
        return 1
    max_id = max(item.get('id', 0) for item in data)
    return max_id + 1


# ==================== CONVENIENCE FUNCTIONS ====================
# These functions provide a simple interface for other modules

def load_users():
    """Load all users from users.json"""
    return load_json(USERS_FILE)


def save_users(users):
    """Save users to users.json"""
    return save_json(USERS_FILE, users)


def load_grievances():
    """Load all grievances from grievances.json"""
    return load_json(GRIEVANCES_FILE)


def save_grievances(grievances):
    """
    Save grievances to both JSON and CSV (dual storage).
    
    Args:
        grievances (list): List of grievance dictionaries
        
    Returns:
        bool: True if successful
    """
    json_ok = save_json(GRIEVANCES_FILE, grievances)
    csv_ok = save_csv(GRIEVANCES_CSV, grievances, GRIEVANCE_CSV_HEADERS)
    return json_ok and csv_ok


def get_next_user_id():
    """Get next available user ID"""
    return get_next_id(USERS_FILE)


def get_next_grievance_id():
    """Get next available grievance ID"""
    return get_next_id(GRIEVANCES_FILE)
