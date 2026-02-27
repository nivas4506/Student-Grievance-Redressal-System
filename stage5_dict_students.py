"""
WEEK 5 - Collections
Dictionary-Based Student Database utilizing sets and tuples
"""

# Dictionary for quick lookup by ID
student_db = {}
# Set for unique IDs
unique_ids = set()
# List of tuples for logs
activity_log = []

def log_activity(action, student_id):
    activity_log.append((action, student_id, "done"))

def add_student():
    sid = input("Enter student ID: ")
    if sid in unique_ids:
        print("Error: ID already exists.")
        return
    
    name = input("Enter student name: ")
    phone = input("Enter student phone: ")
    dept = input("Enter student department: ")
    
    student_db[sid] = {
        "name": name,
        "phone": phone,
        "department": dept,
        "grievances": []
    }
    unique_ids.add(sid)
    log_activity("ADD_STUDENT", sid)
    print("Added successfully.")

def view_students():
    print("\n--- Student Database ---")
    if not student_db:
        print("Empty.")
        return
        
    for sid, data in student_db.items():
        print(f"ID: {sid} | Name: {data['name']} | Dept: {data['department']} | Grievances: len({len(data['grievances'])})")

def show_logs():
    print("\n--- Activity Logs ---")
    if not activity_log:
        print("No activities logged.")
        
    for log in activity_log:
        print(f"Action: {log[0]}, User ID: {log[1]}, Status: {log[2]}")

def main():
    while True:
        print("\n--- Collection Based System ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Show Logs")
        print("4. Exit")
        choice = input("Choice: ")
        
        if choice == '1': add_student()
        elif choice == '2': view_students()
        elif choice == '3': show_logs()
        elif choice == '4': break
        else: print("Invalid")

if __name__ == "__main__":
    main()
