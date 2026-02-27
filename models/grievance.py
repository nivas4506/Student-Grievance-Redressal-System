"""
Grievance Class
Represents a grievance submitted by a student.
Demonstrates: OOP, Inheritance, State Management
"""

from models.record import Record
from datetime import datetime


class Grievance(Record):
    """
    Grievance class representing a complaint/issue.
    Inherits from Record for timestamp functionality.
    """
    
    # Class-level constants
    CATEGORIES = ["Academic", "Hostel", "Faculty", "Infrastructure", "Administrative", "Other"]
    STATUS_OPTIONS = ["Pending", "In Progress", "Resolved", "Rejected"]
    
    def __init__(self, grievance_id=None, student_id=None, student_name="",
                 category="", description=""):
        """
        Initialize a Grievance object.
        
        Args:
            grievance_id (int): Unique grievance identifier
            student_id (int): ID of student who submitted
            student_name (str): Name of the student
            category (str): Grievance category
            description (str): Detailed description
        """
        super().__init__()
        self._grievance_id = grievance_id
        self._student_id = student_id
        self._student_name = student_name
        self._category = category
        self._description = description
        self._status = "Pending"
        self._response = ""
        self._resolved_at = None
    
    # Properties
    @property
    def grievance_id(self):
        """Get grievance ID."""
        return self._grievance_id
    
    @grievance_id.setter
    def grievance_id(self, value):
        """Set grievance ID."""
        self._grievance_id = value
    
    @property
    def student_id(self):
        """Get student ID."""
        return self._student_id
    
    @property
    def student_name(self):
        """Get student name."""
        return self._student_name
    
    @property
    def category(self):
        """Get category."""
        return self._category
    
    @category.setter
    def category(self, value):
        """Set category with validation."""
        if value in self.CATEGORIES:
            self._category = value
        else:
            raise ValueError(f"Invalid category. Must be one of: {self.CATEGORIES}")
    
    @property
    def description(self):
        """Get description."""
        return self._description
    
    @description.setter
    def description(self, value):
        """Set description with validation."""
        if len(value) >= 10:
            self._description = value
        else:
            raise ValueError("Description must be at least 10 characters")
    
    @property
    def status(self):
        """Get current status."""
        return self._status
    
    @property
    def response(self):
        """Get admin response."""
        return self._response
    
    def update_status(self, new_status):
        """
        Update grievance status.
        
        Args:
            new_status (str): New status value
            
        Returns:
            bool: True if successful
        """
        if new_status in self.STATUS_OPTIONS:
            self._status = new_status
            self.update_timestamp()
            
            if new_status == "Resolved":
                self._resolved_at = datetime.now()
            
            return True
        return False
    
    def add_response(self, response):
        """
        Add admin response to grievance.
        
        Args:
            response (str): Response text
        """
        self._response = response
        self.update_timestamp()
    
    def is_resolved(self):
        """Check if grievance is resolved."""
        return self._status == "Resolved"
    
    def is_pending(self):
        """Check if grievance is still pending."""
        return self._status == "Pending"
    
    def get_preview(self, length=30):
        """
        Get preview of description.
        
        Args:
            length (int): Maximum preview length
            
        Returns:
            str: Truncated description
        """
        if len(self._description) > length:
            return self._description[:length-3] + "..."
        return self._description
    
    def to_dict(self):
        """
        Convert grievance to dictionary for storage.
        
        Returns:
            dict: Dictionary representation
        """
        data = super().to_dict()
        data.update({
            'id': self._grievance_id,
            'student_id': self._student_id,
            'student_name': self._student_name,
            'category': self._category,
            'description': self._description,
            'status': self._status,
            'response': self._response,
            'resolved_at': self._resolved_at.strftime("%Y-%m-%d %H:%M:%S") if self._resolved_at else ""
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create Grievance from dictionary.
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Grievance: New Grievance instance
        """
        grievance = cls(
            grievance_id=data.get('id'),
            student_id=data.get('student_id'),
            student_name=data.get('student_name', ''),
            category=data.get('category', 'Other'),
            description=data.get('description', '')
        )
        
        grievance._status = data.get('status', 'Pending')
        grievance._response = data.get('response', '')
        
        if data.get('resolved_at'):
            try:
                grievance._resolved_at = datetime.strptime(data['resolved_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    grievance._resolved_at = datetime.strptime(data['resolved_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        
        if 'created_at' in data and data['created_at']:
            try:
                grievance.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    grievance.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        
        if 'updated_at' in data and data['updated_at']:
            try:
                grievance.updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    grievance.updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        
        return grievance
    
    def __repr__(self):
        return f"Grievance(id={self._grievance_id}, category='{self._category}', status='{self._status}')"
    
    def __str__(self):
        return f"[{self._grievance_id}] {self._category}: {self.get_preview(50)}"
