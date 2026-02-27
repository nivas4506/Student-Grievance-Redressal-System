"""
WEEK 7 - OOP Principles: Encapsulation & Inheritance
Record Base Class & Inherited Grievance Class
"""

from datetime import datetime

class Record:
    """Base class providing timestamps"""
    def __init__(self):
        self._created_at = datetime.now()  # Protected attribute
        self._updated_at = datetime.now()

    def update_timestamp(self):
        self._updated_at = datetime.now()

    def get_timestamps(self):
        return {
            "created": self._created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated": self._updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Grievance(Record):
    """Inherited from Record, demonstrates Encapsulation on status"""
    def __init__(self, student_name, category, description):
        super().__init__()  # Initialize Record constructor
        self.student_name = student_name
        self.category = category
        self.description = description
        self.__status = "Submitted"  # Private attribute (Encapsulation)

    # Getter for status
    def get_status(self):
        return self.__status

    # Setter for status
    def set_status(self, new_status):
        valid_statuses = ["Submitted", "Under Review", "In Process", "Resolved", "Rejected"]
        if new_status in valid_statuses:
            self.__status = new_status
            self.update_timestamp()
            print(f"Status successfully updated to: {self.__status}")
        else:
            print(f"Invalid Status! Allowed: {valid_statuses}")

    def display_details(self):
        print("\n--- Grievance Details ---")
        print(f"Student     : {self.student_name}")
        print(f"Category    : {self.category}")
        print(f"Description : {self.description}")
        print(f"Status      : {self.get_status()} (Encapsulated)")
        print(f"Timestamps  : {self.get_timestamps()['updated']}")


if __name__ == "__main__":
    g1 = Grievance("Nivas", "Academic", "Missing mid-term results in portal.")
    g1.display_details()
    
    # Update Status (Triggers inheritance timestamp update)
    g1.set_status("In Process")
    g1.display_details()
