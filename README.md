# Student Grievance Redressal System

A web-based application for students to submit grievances and administrators to manage and resolve them. Built with Python and Flask.

## Features

### Student Features
- Register and login
- Submit grievances with category selection
- Track grievance status (Pending → In Progress → Resolved)
- View admin responses

### Admin Features
- View all grievances
- Search and filter by status/category
- Update grievance status
- Add responses to grievances
- Delete grievances
- View statistics dashboard

## Tech Stack

- **Backend:** Python, Flask
- **Database:** JSON file storage
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Authentication:** Session-based with SHA-256 password hashing

## Project Structure

```
├── app.py              # Flask web application
├── main.py             # CLI version (alternative)
├── auth.py             # Authentication functions
├── student.py          # Student operations
├── admin.py            # Admin operations
├── file_handler.py     # JSON file handling
├── data/
│   ├── users.json      # User accounts
│   └── grievances.json # Grievances data
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── student_dashboard.html
    ├── submit_grievance.html
    ├── view_grievance.html
    ├── admin_dashboard.html
    └── admin_grievance.html
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nivas4506/Student-Grievance-Redressal-System.git
   cd Student-Grievance-Redressal-System
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install flask
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open browser and go to: `http://127.0.0.1:5000`

## Default Login Credentials

| Role    | Email              | Password |
|---------|--------------------|----------|
| Admin   | admin@college.com  | 123456   |
| Student | Register new account | -      |

## Grievance Categories

- Academic
- Hostel
- Faculty
- Infrastructure
- Administrative
- Other

## Screenshots

### Home Page
Students can login or register to submit grievances.

### Student Dashboard
View submitted grievances and their status.

### Admin Dashboard
Manage all grievances with search and filter options.

## Python Concepts Demonstrated

- Functions and modules
- File handling (JSON read/write)
- Data structures (dictionaries, lists)
- Loops and conditionals
- Input validation
- Password hashing (hashlib)
- Web development with Flask
- Template rendering with Jinja2

## Contributors

- Nivas

## License

This project is for educational purposes.
