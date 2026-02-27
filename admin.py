"""
Admin Module
Handles all administrator operations for managing grievances.
Demonstrates: OOP (Admin, Grievance classes), functions, searching, filtering, CRUD operations
"""

from datetime import datetime
from file_handler import load_grievances, save_grievances
from models import Grievance, Admin

# Use class-level constants from Grievance model
CATEGORIES = {
    "1": "Academic",
    "2": "Hostel",
    "3": "Faculty",
    "4": "Infrastructure",
    "5": "Administrative",
    "6": "Other"
}
STATUS_OPTIONS = Grievance.STATUS_OPTIONS


def view_all_grievances():
    """
    Get all grievances in the system.
    
    Returns:
        list: All grievances
    """
    return load_grievances()


def display_all_grievances(grievances=None):
    """
    Display all grievances in a formatted table.
    
    Args:
        grievances (list, optional): List of grievances to display. 
                                     If None, loads all grievances.
    """
    if grievances is None:
        grievances = view_all_grievances()
    
    if not grievances:
        print("\n[INFO] No grievances found.")
        return
    
    print("\n" + "="*110)
    print(f"{'ID':<6}{'Student':<20}{'Category':<15}{'Status':<15}{'Date':<20}{'Description':<30}")
    print("="*110)
    
    for g in grievances:
        desc_preview = g['description'][:27] + "..." if len(g['description']) > 30 else g['description']
        desc_preview = desc_preview.replace('\n', ' ')
        student_name = g['student_name'][:17] + "..." if len(g['student_name']) > 20 else g['student_name']
        print(f"{g['id']:<6}{student_name:<20}{g['category']:<15}{g['status']:<15}{g['created_at']:<20}{desc_preview:<30}")
    
    print("="*110)
    print(f"Total: {len(grievances)} grievance(s)")


def search_grievances(keyword):
    """
    Search grievances by keyword in description, category, or student name.
    
    Args:
        keyword (str): Search keyword
        
    Returns:
        list: Matching grievances
    """
    grievances = load_grievances()
    keyword = keyword.lower()
    
    results = []
    for g in grievances:
        if (keyword in g['description'].lower() or
            keyword in g['category'].lower() or
            keyword in g['student_name'].lower() or
            keyword in g['status'].lower()):
            results.append(g)
    
    return results


def filter_by_status(status):
    """
    Filter grievances by status.
    
    Args:
        status (str): Status to filter by
        
    Returns:
        list: Grievances with matching status
    """
    grievances = load_grievances()
    return [g for g in grievances if g['status'].lower() == status.lower()]


def filter_by_category(category):
    """
    Filter grievances by category.
    
    Args:
        category (str): Category to filter by
        
    Returns:
        list: Grievances with matching category
    """
    grievances = load_grievances()
    return [g for g in grievances if g['category'].lower() == category.lower()]


def get_grievance_by_id(grievance_id):
    """
    Get a specific grievance by ID.
    
    Args:
        grievance_id (int): ID of the grievance
        
    Returns:
        dict or None: Grievance if found, None otherwise
    """
    grievances = load_grievances()
    for g in grievances:
        if g['id'] == grievance_id:
            return g
    return None


def update_grievance_status(grievance_id, new_status):
    """
    Update the status of a grievance using OOP Grievance class.
    
    Args:
        grievance_id (int): ID of the grievance
        new_status (str): New status to set
        
    Returns:
        tuple: (success: bool, message: str)
        
    Demonstrates: OOP - converting dict to Grievance object, using class methods
    """
    grievances = load_grievances()
    
    for i, g in enumerate(grievances):
        if g['id'] == grievance_id:
            # Convert to Grievance object for OOP operations
            grievance_obj = Grievance.from_dict(g)
            success, message = grievance_obj.update_status(new_status)
            
            if success:
                # Convert back to dict and save
                grievances[i] = grievance_obj.to_dict()
                if save_grievances(grievances):
                    return True, message
                else:
                    return False, "Error saving changes."
            return False, message
    
    return False, "Grievance not found."


def add_response(grievance_id, response_text):
    """
    Add or update admin response to a grievance using OOP Grievance class.
    
    Args:
        grievance_id (int): ID of the grievance
        response_text (str): Response text from admin
        
    Returns:
        tuple: (success: bool, message: str)
        
    Demonstrates: OOP - Grievance.add_response() method
    """
    grievances = load_grievances()
    
    for i, g in enumerate(grievances):
        if g['id'] == grievance_id:
            # Convert to Grievance object for OOP operations
            grievance_obj = Grievance.from_dict(g)
            success, message = grievance_obj.add_response(response_text)
            
            if success:
                grievances[i] = grievance_obj.to_dict()
                if save_grievances(grievances):
                    return True, message
                else:
                    return False, "Error saving response."
            return False, message
    
    return False, "Grievance not found."


def delete_grievance(grievance_id):
    """
    Delete a grievance from the system.
    
    Args:
        grievance_id (int): ID of the grievance to delete
        
    Returns:
        tuple: (success: bool, message: str)
    """
    grievances = load_grievances()
    
    for i, g in enumerate(grievances):
        if g['id'] == grievance_id:
            deleted = grievances.pop(i)
            if save_grievances(grievances):
                return True, f"Grievance #{grievance_id} deleted successfully."
            else:
                return False, "Error saving changes."
    
    return False, "Grievance not found."


def display_grievance_detail_admin(grievance):
    """
    Display detailed view of a grievance for admin.
    
    Args:
        grievance (dict): Grievance dictionary
    """
    if not grievance:
        print("\n[ERROR] Grievance not found.")
        return
    
    print("\n" + "="*60)
    print("            GRIEVANCE DETAILS")
    print("="*60)
    print(f"  Grievance ID  : {grievance['id']}")
    print(f"  Student Name  : {grievance['student_name']}")
    print(f"  Student ID    : {grievance['student_id']}")
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


def get_statistics():
    """
    Get overall statistics of all grievances.
    
    Returns:
        dict: Statistics dictionary
    """
    grievances = load_grievances()
    
    stats = {
        "total": len(grievances),
        "pending": 0,
        "in_progress": 0,
        "resolved": 0,
        "rejected": 0,
        "by_category": {}
    }
    
    for g in grievances:
        # Count by status
        status = g['status'].lower().replace(' ', '_')
        if status in stats:
            stats[status] += 1
        
        # Count by category
        category = g['category']
        if category in stats['by_category']:
            stats['by_category'][category] += 1
        else:
            stats['by_category'][category] = 1
    
    return stats


def display_statistics():
    """Display statistics dashboard for admin."""
    stats = get_statistics()
    
    print("\n" + "="*50)
    print("          GRIEVANCE STATISTICS")
    print("="*50)
    print(f"\n  Total Grievances    : {stats['total']}")
    print("-"*50)
    print("  BY STATUS:")
    print(f"    Pending           : {stats['pending']}")
    print(f"    In Progress       : {stats['in_progress']}")
    print(f"    Resolved          : {stats['resolved']}")
    print(f"    Rejected          : {stats['rejected']}")
    print("-"*50)
    print("  BY CATEGORY:")
    
    if stats['by_category']:
        for category, count in stats['by_category'].items():
            print(f"    {category:<18}: {count}")
    else:
        print("    [No data]")
    
    print("="*50)


def display_status_menu():
    """Display status options for updating."""
    print("\n--- Status Options ---")
    for i, status in enumerate(STATUS_OPTIONS, 1):
        print(f"  {i}. {status}")
    print()


def display_filter_menu():
    """Display filter options."""
    print("\n--- Filter By ---")
    print("  1. Status")
    print("  2. Category")
    print("  3. Show All")
    print()
