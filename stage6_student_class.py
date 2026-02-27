"""
WEEK 6 - OOP: Classes, Objects, Constructors
Student Class implementation
"""

class Student:
    def __init__(self, name, age, phone, department):
        self.name = name
        self.age = age
        self.phone = phone
        self.department = department
        self.grievances = []

    def update_grievance(self, grievance):
        self.grievances.append(grievance)
        print(f"Grievance updated for {self.name}.")

    def display_grievance(self):
        print(f"\n--- {self.name}'s Grievances ---")
        if not self.grievances:
            print("No grievances submitted.")
        else:
            for idx, g in enumerate(self.grievances, 1):
                print(f"{idx}. {g}")

if __name__ == "__main__":
    student1 = Student("Nivas", 21, "9876543210", "Computer Science")
    student1.display_grievance()
    
    student1.update_grievance("Hostel Wi-Fi is frequently disconnecting.")
    student1.update_grievance("Delay in examination results.")
    
    student1.display_grievance()
