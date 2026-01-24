"""
File Handler Module
Handles all JSON file operations for data persistence.
Demonstrates: File handling, JSON operations, error handling
"""

import json
import os

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
GRIEVANCES_FILE = os.path.join(DATA_DIR, 'grievances.json')


def initialize_data_files():
    """
    Create data directory and JSON files if they don't exist.
    Also creates a default admin account.
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
                "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # 'admin' hashed
                "role": "admin",
                "created_at": "2026-01-24"
            }
        ]
        save_data(USERS_FILE, default_users)
        print("[INFO] Created users.json with default admin account.")
        print("       Default Admin: admin@college.com / admin")
    
    # Initialize grievances.json
    if not os.path.exists(GRIEVANCES_FILE):
        save_data(GRIEVANCES_FILE, [])
        print("[INFO] Created grievances.json")


def load_data(filepath):
    """
    Load data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: Data loaded from file, or empty list if file doesn't exist
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


def save_data(filepath, data):
    """
    Save data to a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        data (list): Data to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Could not save data: {e}")
        return False


def get_next_id(filepath):
    """
    Get the next available ID for a new record.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        int: Next available ID
    """
    data = load_data(filepath)
    if not data:
        return 1
    max_id = max(item.get('id', 0) for item in data)
    return max_id + 1


def load_users():
    """Load all users from users.json"""
    return load_data(USERS_FILE)


def save_users(users):
    """Save users to users.json"""
    return save_data(USERS_FILE, users)


def load_grievances():
    """Load all grievances from grievances.json"""
    return load_data(GRIEVANCES_FILE)


def save_grievances(grievances):
    """Save grievances to grievances.json"""
    return save_data(GRIEVANCES_FILE, grievances)


def get_next_user_id():
    """Get next available user ID"""
    return get_next_id(USERS_FILE)


def get_next_grievance_id():
    """Get next available grievance ID"""
    return get_next_id(GRIEVANCES_FILE)
