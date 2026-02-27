"""
Admin Class
Represents an administrator user with management capabilities.
Demonstrates: OOP, Inheritance, Polymorphism
"""

from models.student import Student


class Admin(Student):
    """
    Admin class representing an administrator user.
    Inherits from Student with additional privileges.
    """
    
    def __init__(self, admin_id=None, name="", email="", password="", dept="Administration"):
        """
        Initialize an Admin object.
        
        Args:
            admin_id (int): Unique admin identifier
            name (str): Admin's full name
            email (str): Admin's email address
            password (str): Hashed password
            dept (str): Department name
        """
        super().__init__(admin_id, name, email, password, dept)
        self._role = "admin"
    
    def assign_grievance(self, grievance, assignee=None):
        """
        Assign a grievance for processing.
        
        Args:
            grievance: Grievance object to assign
            assignee: Person to assign to (optional)
            
        Returns:
            bool: True if successful
        """
        if grievance.is_pending():
            grievance.update_status("In Progress")
            return True
        return False
    
    def update_grievance_status(self, grievance, status):
        """
        Update the status of a grievance.
        
        Args:
            grievance: Grievance object
            status (str): New status
            
        Returns:
            bool: True if successful
        """
        return grievance.update_status(status)
    
    def add_grievance_response(self, grievance, response):
        """
        Add a response to a grievance.
        
        Args:
            grievance: Grievance object
            response (str): Response text
        """
        grievance.add_response(response)
    
    def resolve_grievance(self, grievance, response=""):
        """
        Mark a grievance as resolved.
        
        Args:
            grievance: Grievance object
            response (str): Optional response text
            
        Returns:
            bool: True if successful
        """
        if response:
            grievance.add_response(response)
        return grievance.update_status("Resolved")
    
    def reject_grievance(self, grievance, reason=""):
        """
        Reject a grievance.
        
        Args:
            grievance: Grievance object
            reason (str): Rejection reason
            
        Returns:
            bool: True if successful
        """
        if reason:
            grievance.add_response(f"Rejected: {reason}")
        return grievance.update_status("Rejected")
    
    def to_dict(self):
        """
        Convert admin to dictionary for storage.
        
        Returns:
            dict: Dictionary representation
        """
        data = super().to_dict()
        data['role'] = 'admin'
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create Admin from dictionary.
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Admin: New Admin instance
        """
        admin = cls(
            admin_id=data.get('id'),
            name=data.get('name', ''),
            email=data.get('email', ''),
            dept=data.get('dept', 'Administration')
        )
        admin._password = data.get('password', '')
        
        if 'created_at' in data and data['created_at']:
            try:
                from datetime import datetime
                admin.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    admin.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        
        return admin
    
    def __repr__(self):
        return f"Admin(id={self._student_id}, name='{self._name}', email='{self._email}')"
