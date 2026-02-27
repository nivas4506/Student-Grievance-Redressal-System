"""
Authentication Module
Handles user registration and login functionality.
Demonstrates: Functions, hashlib, OOP integration, data structures (dictionaries)
"""

import hashlib
from datetime import date
from file_handler import load_users, save_users, get_next_user_id
from models import Student, Admin


def hash_password(password):
    """
    Hash a password using SHA-256.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
        
    Demonstrates: hashlib module, string encoding
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    """
    Basic email validation.
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid format, False otherwise
        
    Demonstrates: String operations, conditional logic
    """
    if '@' in email and '.' in email and len(email) > 5:
        return True
    return False


def email_exists(email):
    """
    Check if an email already exists in the system.
    
    Args:
        email (str): Email to check
        
    Returns:
        bool: True if exists, False otherwise
        
    Demonstrates: List iteration, string comparison
    """
    users = load_users()
    for user in users:
        if user['email'].lower() == email.lower():
            return True
    return False


def register_user(name, email, password, role="student", dept="General"):
    """
    Register a new user in the system using OOP classes.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password
        role (str): User role - 'student' or 'admin'
        dept (str): Department name (for students)
        
    Returns:
        tuple: (success: bool, message: str)
        
    Demonstrates: OOP object creation, validation, file storage
    """
    # Validate inputs
    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters."
    
    if not validate_email(email):
        return False, "Invalid email format."
    
    if email_exists(email):
        return False, "Email already registered."
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    
    # Create user object using OOP classes
    user_id = get_next_user_id()
    password_hash = hash_password(password)
    
    if role == "admin":
        user_obj = Admin(
            admin_id=user_id,
            name=name.strip(),
            email=email.lower().strip(),
            password=password_hash
        )
    else:
        user_obj = Student(
            student_id=user_id,
            name=name.strip(),
            email=email.lower().strip(),
            password=password_hash,
            dept=dept
        )
    
    # Convert to dict and save
    users = load_users()
    user_dict = user_obj.to_dict()
    user_dict['created_at'] = str(date.today())
    users.append(user_dict)
    
    if save_users(users):
        return True, f"Registration successful! Welcome, {name}."
    else:
        return False, "Error saving user data."


def login_user(email, password):
    """
    Authenticate a user.
    
    Args:
        email (str): User's email
        password (str): User's password
        
    Returns:
        tuple: (success: bool, user_data: dict or error_message: str)
        
    Demonstrates: Authentication, password hashing comparison
    """
    users = load_users()
    hashed_password = hash_password(password)
    
    for user in users:
        if user['email'].lower() == email.lower():
            if user['password'] == hashed_password:
                # Return user data without password
                user_data = {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email'],
                    "role": user['role'],
                    "dept": user.get('dept', 'General')
                }
                return True, user_data
            else:
                return False, "Incorrect password."
    
    return False, "Email not found. Please register first."


def get_user_by_id(user_id):
    """
    Get user details by their ID.
    
    Args:
        user_id (int): User's ID
        
    Returns:
        dict or None: User data if found, None otherwise
    """
    users = load_users()
    for user in users:
        if user['id'] == user_id:
            return {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],
                "dept": user.get('dept', 'General')
            }
    return None

