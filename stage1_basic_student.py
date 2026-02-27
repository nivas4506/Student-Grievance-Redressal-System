"""
WEEK 1 - Python Foundations
Basic Student Entry Script
Accepts student details and grievance, then prints them.
"""

def main():
    print("--- Basic Student Data Capture ---")
    name = input("Enter student name: ")
    roll_no = input("Enter student ID / Roll Number: ")
    dept = input("Enter department: ")
    
    print("\nGrievance Categories: Academic / Exam / Hostel / Fees / Others")
    category = input("Enter grievance category: ")
    description = input("Enter grievance description: ")
    
    print("\n--- Grievance Record ---")
    print(f"Name         : {name}")
    print(f"Roll Number  : {roll_no}")
    print(f"Department   : {dept}")
    print(f"Category     : {category}")
    print(f"Description  : {description}")

if __name__ == "__main__":
    main()
