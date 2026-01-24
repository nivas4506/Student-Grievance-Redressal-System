"""
Student Module
Handles all student-related operations for grievance submission and tracking.
Demonstrates: Functions, lists, dictionaries, iteration, filtering
"""

from datetime import datetime
from file_handler import load_grievances, save_grievances, get_next_grievance_id

# Grievance categories
CATEGORIES = {
    "1": "Academic",
    "2": "Hostel",
    "3": "Faculty",
    "4": "Infrastructure",
    "5": "Administrative",
    "6": "Other"
}

# Status options
STATUS_OPTIONS = ["Pending", "In Progress", "Resolved", "Rejected"]


def display_categories():
    """Display available grievance categories."""
    print("\n--- Grievance Categories ---")
    for key, value in CATEGORIES.items():
        print(f"  {key}. {value}")
    print()


def submit_grievance(student_id, student_name):
    """
    Submit a new grievance.
    
    Args:
        student_id (int): ID of the student submitting
        student_name (str): Name of the student
        
    Returns:
        tuple: (success: bool, message: str)
    """
    print("\n" + "="*50)
    print("         SUBMIT NEW GRIEVANCE")
    print("="*50)
    
    # Select category
    display_categories()
    category_choice = input("Select category (1-6): ").strip()
    
    if category_choice not in CATEGORIES:
        return False, "Invalid category selected."
    
    category = CATEGORIES[category_choice]
    
    # Get grievance description
    print("\nDescribe your grievance in detail:")
    print("(Type your grievance and press Enter twice to finish)")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    description = "\n".join(lines)
    
    if len(description) < 10:
        return False, "Description must be at least 10 characters."
    
    # Create grievance dictionary
    grievances = load_grievances()
    new_grievance = {
        "id": get_next_grievance_id(),
        "student_id": student_id,
        "student_name": student_name,
        "category": category,
        "description": description,
        "status": "Pending",
        "response": "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "resolved_at": ""
    }
    
    # Save grievance
    grievances.append(new_grievance)
    if save_grievances(grievances):
        return True, f"Grievance submitted successfully! Your Grievance ID is: {new_grievance['id']}"
    else:
        return False, "Error saving grievance."


def view_my_grievances(student_id):
    """
    View all grievances submitted by a student.
    
    Args:
        student_id (int): ID of the student
        
    Returns:
        list: List of grievances belonging to the student
    """
    grievances = load_grievances()
    my_grievances = [g for g in grievances if g['student_id'] == student_id]
    return my_grievances


def display_grievances_table(grievances):
    """
    Display grievances in a formatted table.
    
    Args:
        grievances (list): List of grievance dictionaries
    """
    if not grievances:
        print("\n[INFO] No grievances found.")
        return
    
    print("\n" + "="*90)
    print(f"{'ID':<6}{'Category':<15}{'Status':<15}{'Date':<20}{'Description':<30}")
    print("="*90)
    
    for g in grievances:
        desc_preview = g['description'][:27] + "..." if len(g['description']) > 30 else g['description']
        desc_preview = desc_preview.replace('\n', ' ')
        print(f"{g['id']:<6}{g['category']:<15}{g['status']:<15}{g['created_at']:<20}{desc_preview:<30}")
    
    print("="*90)
    print(f"Total: {len(grievances)} grievance(s)")


def view_grievance_detail(grievance_id, student_id):
    """
    View detailed information about a specific grievance.
    
    Args:
        grievance_id (int): ID of the grievance
        student_id (int): ID of the student (for verification)
        
    Returns:
        dict or None: Grievance details if found and belongs to student
    """
    grievances = load_grievances()
    
    for g in grievances:
        if g['id'] == grievance_id:
            # Verify ownership
            if g['student_id'] != student_id:
                return None
            return g
    
    return None


def display_grievance_detail(grievance):
    """
    Display detailed view of a single grievance.
    
    Args:
        grievance (dict): Grievance dictionary
    """
    if not grievance:
        print("\n[ERROR] Grievance not found or access denied.")
        return
    
    print("\n" + "="*60)
    print("            GRIEVANCE DETAILS")
    print("="*60)
    print(f"  Grievance ID  : {grievance['id']}")
    print(f"  Category      : {grievance['category']}")
    print(f"  Status        : {grievance['status']}")
    print(f"  Submitted On  : {grievance['created_at']}")
    
    if grievance['updated_at']:
        print(f"  Last Updated  : {grievance['updated_at']}")
    
    if grievance['resolved_at']:
        print(f"  Resolved On   : {grievance['resolved_at']}")
    
    print("-"*60)
    print("  Description:")
    print("-"*60)
    # Indent description
    for line in grievance['description'].split('\n'):
        print(f"    {line}")
    
    print("-"*60)
    print("  Admin Response:")
    print("-"*60)
    if grievance['response']:
        for line in grievance['response'].split('\n'):
            print(f"    {line}")
    else:
        print("    [No response yet]")
    
    print("="*60)


def get_status_summary(student_id):
    """
    Get summary statistics of grievances for a student.
    
    Args:
        student_id (int): ID of the student
        
    Returns:
        dict: Summary with counts by status
    """
    grievances = view_my_grievances(student_id)
    
    summary = {
        "total": len(grievances),
        "pending": 0,
        "in_progress": 0,
        "resolved": 0,
        "rejected": 0
    }
    
    for g in grievances:
        status = g['status'].lower().replace(' ', '_')
        if status in summary:
            summary[status] += 1
    
    return summary


def display_status_summary(student_id):
    """
    Display status summary for a student.
    
    Args:
        student_id (int): ID of the student
    """
    summary = get_status_summary(student_id)
    
    print("\n" + "-"*40)
    print("        YOUR GRIEVANCES SUMMARY")
    print("-"*40)
    print(f"  Total Grievances  : {summary['total']}")
    print(f"  Pending           : {summary['pending']}")
    print(f"  In Progress       : {summary['in_progress']}")
    print(f"  Resolved          : {summary['resolved']}")
    print(f"  Rejected          : {summary['rejected']}")
    print("-"*40)
