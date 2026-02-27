"""
WEEK 11 - Exceptions & Robust Validation
Input Validation and Custom Exceptions
"""

class GrievanceSystemError(Exception):
    """Base exception for Grievance System."""
    pass

class InvalidStudentError(GrievanceSystemError):
    """Raised when student details are invalid."""
    pass

class InvalidGrievanceError(GrievanceSystemError):
    """Raised when grievance details are invalid."""
    pass

def validate_student_id(student_id):
    if not isinstance(student_id, str) or not student_id.strip():
        raise InvalidStudentError("Student ID cannot be empty.")
    if len(student_id) < 3:
        raise InvalidStudentError("Student ID must be at least 3 characters.")
    return True

def validate_name(name):
    if not name or not name.replace(" ", "").isalpha():
        raise InvalidStudentError("Name must contain only alphabets and spaces.")
    if len(name) < 2:
        raise InvalidStudentError("Name must be at least 2 characters long.")
    return True

def validate_category(category):
    valid_categories = {"Academic", "Examination", "Hostel", "Transport", "Administration", "Others"}
    if category not in valid_categories:
        raise InvalidGrievanceError(f"Category '{category}' is invalid. Choose from {valid_categories}")
    return True

def validate_description(description):
    if not description or len(description.strip()) < 10:
        raise InvalidGrievanceError("Grievance description must be at least 10 characters long.")
    return True

def safe_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Error: Please enter a valid integer.")
