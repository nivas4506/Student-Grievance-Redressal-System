"""
WEEK 2 - Conditionals & Loops
Interactive Menu System for Grievances
"""

def main():
    students = []
    
    while True:
        print("\n--- Student Menu Shell ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            roll_no = input("Enter student ID/roll no: ")
            students.append(f"{name} ({roll_no})")
            print("Student added successfully.")
        elif choice == '2':
            print("\n--- Student List ---")
            if not students:
                print("No students found.")
            else:
                for idx, student in enumerate(students, 1):
                    print(f"{idx}. {student}")
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
