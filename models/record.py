"""
Record Base Class
Base class for all records in the system.
Demonstrates: OOP, Inheritance, datetime handling
"""

from datetime import datetime


class Record:
    """
    Base class for all records.
    Provides common timestamp functionality.
    """
    
    def __init__(self):
        """Initialize record with timestamps."""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
    
    def get_created_date(self):
        """Get formatted creation date."""
        return self.created_at.strftime("%Y-%m-%d")
    
    def get_updated_date(self):
        """Get formatted update date."""
        return self.updated_at.strftime("%Y-%m-%d")
    
    def to_dict(self):
        """
        Convert record to dictionary.
        Should be overridden by subclasses.
        
        Returns:
            dict: Dictionary representation of record
        """
        return {
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self.created_at, 'strftime') else str(self.created_at),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(self.updated_at, 'strftime') else str(self.updated_at)
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create record from dictionary.
        Should be overridden by subclasses.
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Record: New record instance
        """
        record = cls()
        if 'created_at' in data and data['created_at']:
            try:
                record.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    record.created_at = datetime.strptime(data['created_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        if 'updated_at' in data and data['updated_at']:
            try:
                record.updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                try:
                    record.updated_at = datetime.strptime(data['updated_at'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    pass
        return record
    
    def __repr__(self):
        return f"Record(created={self.get_created_date()})"
