"""
Student Class
Represents a student user in the system.
Demonstrates: OOP, Inheritance, Encapsulation
"""

from models.record import Record
import hashlib


class Student(Record):
    """
    Student class representing a student user.
    Inherits from Record for timestamp functionality.
    """
    
    def __init__(self, student_id=None, name="", email="", password="", dept=""):
        """
        Initialize a Student object.
        
        Args:
            student_id (int): Unique student identifier
            name (str): Student's full name
            email (str): Student's email address
            password (str): Hashed password
            dept (str): Department name
        """
        super().__init__()
        self._student_id = student_id
        self._name = name
        self._email = email
        self._password = password
        self._dept = dept
        self._role = "student"
    
    # Properties for encapsulation
    @property
    def student_id(self):
        """Get student ID."""
        return self._student_id
    
    @student_id.setter
    def student_id(self, value):
        """Set student ID."""
        self._student_id = value
    
    @property
    def name(self):
        """Get student name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set student name."""
        if len(value) >= 2:
            self._name = value
        else:
            raise ValueError("Name must be at least 2 characters")
    
    @property
    def email(self):
        """Get student email."""
        return self._email
    
    @email.setter
    def email(self, value):
        """Set student email."""
        if '@' in value and '.' in value:
            self._email = value.lower()
        else:
            raise ValueError("Invalid email format")
    
    @property
    def dept(self):
        """Get department."""
        return self._dept
    
    @dept.setter
    def dept(self, value):
        """Set department."""
        self._dept = value
    
    @property
    def role(self):
        """Get user role."""
        return self._role
    
    def set_password(self, password):
        """
        Set password (hashed).
        
        Args:
            password (str): Plain text password
        """
        if len(password) >= 4:
            self._password = hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError("Password must be at least 4 characters")
    
    def verify_password(self, password):
        """
        Verify password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches
        """
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self._password
    
    def to_dict(self):
        """
        Convert student to dictionary for storage.
        
        Returns:
            dict: Dictionary representation
        """
        data = super().to_dict()
        data.update({
            'id': self._student_id,
            'name': self._name,
            'email': self._email,
            'password': self._password,
            'dept': self._dept,
            'role': self._role
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create Student from dictionary.
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Student: New Student instance
        """
        student = cls(
            student_id=data.get('id'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            dept=data.get('dept', '')
        )
        student._password = data.get('password', '')
        student._role = data.get('role', 'student')
        
        if 'created_at' in data and data['created_at']:
            try:
                from datetime import datetime
                student.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    student.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        
        return student
    
    def __repr__(self):
        return f"Student(id={self._student_id}, name='{self._name}', email='{self._email}')"
    
    def __str__(self):
        return f"{self._name} ({self._email})"
