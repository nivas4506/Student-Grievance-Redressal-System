"""
WEEK 10 Core Logic Module
"""
from .utils import log_action  # Relative Import example

def process_grievance(student, text):
    log_action("Processing Grievance Workflow")
    print(f"[{student}] Grievance logic processed: {text}")
    return True
