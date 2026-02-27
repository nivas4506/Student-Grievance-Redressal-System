"""
WEEK 3 - Strings & Lists
Student Storage and Search functionality
"""

def main():
    students = []
    
    while True:
        print("\n--- Student Search & Listing ---")
        print("1. Add Student Grievance")
        print("2. Search Student")
        print("3. View All Students")
        print("4. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            name = input("Enter student name: ")
            roll_no = input("Enter student ID: ")
            dept = input("Enter department: ")
            
            # Dictionary representing a student record
            record = {
                "name": name,
                "id": roll_no,
                "dept": dept
            }
            students.append(record)
            print("Record added!")
            
        elif choice == '2':
            search_query = input("Enter student ID or name to search: ")
            found = False
            for student in students:
                if search_query.lower() in student["id"].lower() or search_query.lower() in student["name"].lower():
                    print("\nRecord Found:")
                    print(f"ID: {student['id']}, Name: {student['name']}, Dept: {student['dept']}")
                    found = True
            if not found:
                print("No matching record found.")
                
        elif choice == '3':
            print("\n" + "-"*40)
            print(f"{'ID':<10} | {'Name':<15} | {'Dept':<10}")
            print("-" * 40)
            for student in students:
                print(f"{student['id']:<10} | {student['name']:<15} | {student['dept']:<10}")
            print("-" * 40)
            
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
