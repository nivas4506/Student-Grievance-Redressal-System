"""
Models Package
Contains base classes for the SGRS system.
"""

from models.record import Record
from models.student import Student
from models.grievance import Grievance
from models.admin import Admin

__all__ = ['Record', 'Student', 'Grievance', 'Admin']
