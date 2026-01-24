"""
Student Grievance Redressal System
Main Entry Point

A menu-driven console application for managing student grievances.
Students can submit and track grievances.
Administrators can view, search, update, and delete grievances.

Demonstrates:
- Python functions and modules
- File handling (JSON)
- Data structures (lists, dictionaries)
- Control flow (loops, conditionals)
- Input validation
"""

import os
import sys

# Import custom modules
from file_handler import initialize_data_files
from auth import register_user, login_user
from student import (
    submit_grievance,
    view_my_grievances,
    display_grievances_table,
    view_grievance_detail,
    display_grievance_detail,
    display_status_summary
)
from admin import (
    view_all_grievances,
    display_all_grievances,
    search_grievances,
    filter_by_status,
    filter_by_category,
    get_grievance_by_id,
    update_grievance_status,
    add_response,
    delete_grievance,
    display_grievance_detail_admin,
    display_statistics,
    display_status_menu,
    display_filter_menu,
    STATUS_OPTIONS,
    CATEGORIES
)


# Global variable to store logged-in user
current_user = None


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause and wait for user input."""
    input("\nPress Enter to continue...")


def display_banner():
    """Display the application banner."""
    print("\n" + "="*60)
    print("     STUDENT GRIEVANCE REDRESSAL SYSTEM")
    print("="*60)
    print("         A platform for students to voice concerns")
    print("         and get them addressed by administration")
    print("="*60)


def display_main_menu():
    """Display the main menu."""
    print("\n--- MAIN MENU ---")
    print("  1. Login")
    print("  2. Register (Student)")
    print("  3. Exit")
    print()


def display_student_menu(user_name):
    """Display the student menu."""
    print(f"\n--- STUDENT MENU --- (Logged in as: {user_name})")
    print("  1. Submit New Grievance")
    print("  2. View My Grievances")
    print("  3. View Grievance Details")
    print("  4. View Summary")
    print("  5. Logout")
    print()


def display_admin_menu(user_name):
    """Display the admin menu."""
    print(f"\n--- ADMIN MENU --- (Logged in as: {user_name})")
    print("  1. View All Grievances")
    print("  2. Search Grievances")
    print("  3. Filter Grievances")
    print("  4. View Grievance Details")
    print("  5. Update Grievance Status")
    print("  6. Add Response to Grievance")
    print("  7. Delete Grievance")
    print("  8. View Statistics")
    print("  9. Logout")
    print()


def handle_login():
    """Handle user login."""
    global current_user
    
    print("\n--- LOGIN ---")
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    success, result = login_user(email, password)
    
    if success:
        current_user = result
        print(f"\n[SUCCESS] Welcome back, {current_user['name']}!")
        return True
    else:
        print(f"\n[ERROR] {result}")
        return False


def handle_register():
    """Handle student registration."""
    print("\n--- STUDENT REGISTRATION ---")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Confirm Password: ").strip()
    
    if password != confirm_password:
        print("\n[ERROR] Passwords do not match.")
        return False
    
    success, message = register_user(name, email, password, "student")
    
    if success:
        print(f"\n[SUCCESS] {message}")
        print("You can now login with your credentials.")
        return True
    else:
        print(f"\n[ERROR] {message}")
        return False


def student_menu_loop():
    """Main loop for student menu."""
    global current_user
    
    while True:
        clear_screen()
        display_banner()
        display_student_menu(current_user['name'])
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            # Submit new grievance
            success, message = submit_grievance(
                current_user['id'],
                current_user['name']
            )
            if success:
                print(f"\n[SUCCESS] {message}")
            else:
                print(f"\n[ERROR] {message}")
            pause()
            
        elif choice == "2":
            # View my grievances
            clear_screen()
            print("\n--- MY GRIEVANCES ---")
            grievances = view_my_grievances(current_user['id'])
            display_grievances_table(grievances)
            pause()
            
        elif choice == "3":
            # View grievance details
            try:
                grievance_id = int(input("\nEnter Grievance ID: ").strip())
                grievance = view_grievance_detail(grievance_id, current_user['id'])
                display_grievance_detail(grievance)
            except ValueError:
                print("\n[ERROR] Invalid ID. Please enter a number.")
            pause()
            
        elif choice == "4":
            # View summary
            display_status_summary(current_user['id'])
            pause()
            
        elif choice == "5":
            # Logout
            print(f"\nGoodbye, {current_user['name']}!")
            current_user = None
            pause()
            break
            
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
            pause()


def admin_menu_loop():
    """Main loop for admin menu."""
    global current_user
    
    while True:
        clear_screen()
        display_banner()
        display_admin_menu(current_user['name'])
        
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == "1":
            # View all grievances
            clear_screen()
            print("\n--- ALL GRIEVANCES ---")
            display_all_grievances()
            pause()
            
        elif choice == "2":
            # Search grievances
            keyword = input("\nEnter search keyword: ").strip()
            if keyword:
                results = search_grievances(keyword)
                print(f"\n--- Search Results for '{keyword}' ---")
                display_all_grievances(results)
            else:
                print("\n[ERROR] Please enter a search keyword.")
            pause()
            
        elif choice == "3":
            # Filter grievances
            display_filter_menu()
            filter_choice = input("Select filter option (1-3): ").strip()
            
            if filter_choice == "1":
                # Filter by status
                display_status_menu()
                try:
                    status_num = int(input("Select status (1-4): ").strip())
                    if 1 <= status_num <= len(STATUS_OPTIONS):
                        status = STATUS_OPTIONS[status_num - 1]
                        results = filter_by_status(status)
                        print(f"\n--- Grievances with status: {status} ---")
                        display_all_grievances(results)
                    else:
                        print("\n[ERROR] Invalid status selection.")
                except ValueError:
                    print("\n[ERROR] Invalid input.")
                    
            elif filter_choice == "2":
                # Filter by category
                print("\n--- Categories ---")
                categories = list(CATEGORIES.values())
                for i, cat in enumerate(categories, 1):
                    print(f"  {i}. {cat}")
                try:
                    cat_num = int(input("\nSelect category (1-6): ").strip())
                    if 1 <= cat_num <= len(categories):
                        category = categories[cat_num - 1]
                        results = filter_by_category(category)
                        print(f"\n--- Grievances in category: {category} ---")
                        display_all_grievances(results)
                    else:
                        print("\n[ERROR] Invalid category selection.")
                except ValueError:
                    print("\n[ERROR] Invalid input.")
                    
            elif filter_choice == "3":
                display_all_grievances()
            else:
                print("\n[ERROR] Invalid filter option.")
            pause()
            
        elif choice == "4":
            # View grievance details
            try:
                grievance_id = int(input("\nEnter Grievance ID: ").strip())
                grievance = get_grievance_by_id(grievance_id)
                display_grievance_detail_admin(grievance)
            except ValueError:
                print("\n[ERROR] Invalid ID. Please enter a number.")
            pause()
            
        elif choice == "5":
            # Update grievance status
            try:
                grievance_id = int(input("\nEnter Grievance ID: ").strip())
                grievance = get_grievance_by_id(grievance_id)
                
                if grievance:
                    print(f"\nCurrent status: {grievance['status']}")
                    display_status_menu()
                    status_num = int(input("Select new status (1-4): ").strip())
                    
                    if 1 <= status_num <= len(STATUS_OPTIONS):
                        new_status = STATUS_OPTIONS[status_num - 1]
                        success, message = update_grievance_status(grievance_id, new_status)
                        if success:
                            print(f"\n[SUCCESS] {message}")
                        else:
                            print(f"\n[ERROR] {message}")
                    else:
                        print("\n[ERROR] Invalid status selection.")
                else:
                    print("\n[ERROR] Grievance not found.")
            except ValueError:
                print("\n[ERROR] Invalid input.")
            pause()
            
        elif choice == "6":
            # Add response to grievance
            try:
                grievance_id = int(input("\nEnter Grievance ID: ").strip())
                grievance = get_grievance_by_id(grievance_id)
                
                if grievance:
                    display_grievance_detail_admin(grievance)
                    print("\nEnter your response (press Enter twice to finish):")
                    lines = []
                    while True:
                        line = input()
                        if line == "":
                            break
                        lines.append(line)
                    
                    response_text = "\n".join(lines)
                    success, message = add_response(grievance_id, response_text)
                    if success:
                        print(f"\n[SUCCESS] {message}")
                    else:
                        print(f"\n[ERROR] {message}")
                else:
                    print("\n[ERROR] Grievance not found.")
            except ValueError:
                print("\n[ERROR] Invalid input.")
            pause()
            
        elif choice == "7":
            # Delete grievance
            try:
                grievance_id = int(input("\nEnter Grievance ID to delete: ").strip())
                grievance = get_grievance_by_id(grievance_id)
                
                if grievance:
                    display_grievance_detail_admin(grievance)
                    confirm = input("\nAre you sure you want to delete this grievance? (yes/no): ").strip().lower()
                    
                    if confirm == "yes":
                        success, message = delete_grievance(grievance_id)
                        if success:
                            print(f"\n[SUCCESS] {message}")
                        else:
                            print(f"\n[ERROR] {message}")
                    else:
                        print("\n[INFO] Deletion cancelled.")
                else:
                    print("\n[ERROR] Grievance not found.")
            except ValueError:
                print("\n[ERROR] Invalid input.")
            pause()
            
        elif choice == "8":
            # View statistics
            clear_screen()
            display_statistics()
            pause()
            
        elif choice == "9":
            # Logout
            print(f"\nGoodbye, {current_user['name']}!")
            current_user = None
            pause()
            break
            
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
            pause()


def main():
    """Main function - entry point of the application."""
    global current_user
    
    # Initialize data files on first run
    initialize_data_files()
    
    while True:
        clear_screen()
        display_banner()
        display_main_menu()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Login
            if handle_login():
                pause()
                # Redirect based on role
                if current_user['role'] == "admin":
                    admin_menu_loop()
                else:
                    student_menu_loop()
            else:
                pause()
                
        elif choice == "2":
            # Register
            handle_register()
            pause()
            
        elif choice == "3":
            # Exit
            clear_screen()
            print("\n" + "="*50)
            print("   Thank you for using the Grievance System!")
            print("               Goodbye!")
            print("="*50 + "\n")
            sys.exit(0)
            
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
            pause()


if __name__ == "__main__":
    main()
