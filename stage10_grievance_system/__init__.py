"""
WEEK 10 - Packages & __init__.py
This file marks the 'stage10_grievance_system' directory as a Python package.
It controls what is exported when someone runs: from stage10_grievance_system import *
"""

from .core_logic import process_grievance
from .utils import format_category

__all__ = ["process_grievance", "format_category"]
__version__ = "1.0.0"

print("[Week 10] Grievance System Package Initialized!")
