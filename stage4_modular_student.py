"""
WEEK 4 - Functions
Modular Student System
"""

students = []

def add_student():
    name = input("Enter student name: ")
    roll_no = input("Enter student ID: ")
    students.append({"id": roll_no, "name": name, "grievances": []})
    print("Student added!")

def search_student(query):
    for s in students:
        if s["id"] == query or query.lower() in s["name"].lower():
            return s
    return None

def update_student():
    sid = input("Enter Student ID to update: ")
    s = search_student(sid)
    if s:
        s["name"] = input(f"Enter new name ({s['name']}): ") or s["name"]
        print("Student updated.")
    else:
        print("Student not found.")

def delete_student():
    sid = input("Enter Student ID to delete: ")
    global students
    students = [s for s in students if s["id"] != sid]
    print("Student deleted if existed.")

def validate_grievance_category(category):
    valid = ["Academic", "Exam", "Hostel", "Fees", "Others"]
    return category in valid

def add_grievance():
    sid = input("Enter Student ID for grievance: ")
    s = search_student(sid)
    if s:
        cat = input("Enter category (Academic/Exam/Hostel/Fees/Others): ")
        if validate_grievance_category(cat):
            desc = input("Enter description: ")
            s["grievances"].append({"category": cat, "description": desc})
            print("Grievance added.")
        else:
            print("Invalid category.")
    else:
        print("Student not found.")

def search_grievance():
    query = input("Enter grievance category or description keyword: ").lower()
    found = False
    for s in students:
        for g in s["grievances"]:
            if query in g["category"].lower() or query in g["description"].lower():
                print(f"Student: {s['name']} | Category: {g['category']} | Desc: {g['description']}")
                found = True
    if not found:
        print("No matching grievances.")

def view_all_grievances():
    if not students:
        print("No records available.")
        return
        
    for s in students:
        if s["grievances"]:
            print(f"\nStudent: {s['name']} ({s['id']})")
            for idx, g in enumerate(s["grievances"], 1):
                print(f"  {idx}. [{g['category']}] {g['description']}")

def main():
    while True:
        print("\n--- Modular System ---")
        print("1. Add Student         2. Search Student    3. Update Student")
        print("4. Delete Student      5. Add Grievance     6. Search Grievance")
        print("7. View All Grievances 8. Exit")
        choice = input("Choice: ")
        if choice == '1': add_student()
        elif choice == '2':
            q = input("Search term: ")
            res = search_student(q)
            print("Found:", res) if res else print("Not found.")
        elif choice == '3': update_student()
        elif choice == '4': delete_student()
        elif choice == '5': add_grievance()
        elif choice == '6': search_grievance()
        elif choice == '7': view_all_grievances()
        elif choice == '8': break
        else: print("Invalid")

if __name__ == "__main__":
    main()
