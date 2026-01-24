"""
Student Grievance Redressal System - Web Version
Simple Flask web application
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

from file_handler import initialize_data_files, load_users, save_users, load_grievances, save_grievances, get_next_user_id, get_next_grievance_id
from auth import hash_password, validate_email, email_exists

app = Flask(__name__)
app.secret_key = 'grievance_system_secret_key_2026'

# Categories and Status options
CATEGORIES = ["Academic", "Hostel", "Faculty", "Infrastructure", "Administrative", "Other"]
STATUS_OPTIONS = ["Pending", "In Progress", "Resolved", "Rejected"]

# Initialize data files
initialize_data_files()


# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page with login/register options"""
    if 'user' in session:
        if session['user']['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('student_dashboard'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        users = load_users()
        hashed = hash_password(password)
        
        for user in users:
            if user['email'].lower() == email and user['password'] == hashed:
                session['user'] = {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
                flash(f'Welcome back, {user["name"]}!', 'success')
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('student_dashboard'))
        
        flash('Invalid email or password.', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        # Validation
        if len(name) < 2:
            flash('Name must be at least 2 characters.', 'error')
        elif not validate_email(email):
            flash('Invalid email format.', 'error')
        elif email_exists(email):
            flash('Email already registered.', 'error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        else:
            users = load_users()
            new_user = {
                'id': get_next_user_id(),
                'name': name,
                'email': email,
                'password': hash_password(password),
                'role': 'student',
                'created_at': str(datetime.now().date())
            }
            users.append(new_user)
            save_users(users)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


# ==================== STUDENT ROUTES ====================

@app.route('/student')
def student_dashboard():
    """Student dashboard"""
    if 'user' not in session or session['user']['role'] != 'student':
        flash('Please login as student.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user']['id']
    grievances = load_grievances()
    my_grievances = [g for g in grievances if g['student_id'] == user_id]
    
    # Stats
    stats = {
        'total': len(my_grievances),
        'pending': len([g for g in my_grievances if g['status'] == 'Pending']),
        'in_progress': len([g for g in my_grievances if g['status'] == 'In Progress']),
        'resolved': len([g for g in my_grievances if g['status'] == 'Resolved'])
    }
    
    return render_template('student_dashboard.html', grievances=my_grievances, stats=stats, user=session['user'])


@app.route('/student/submit', methods=['GET', 'POST'])
def submit_grievance():
    """Submit new grievance"""
    if 'user' not in session or session['user']['role'] != 'student':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form.get('category', '')
        description = request.form.get('description', '').strip()
        
        if category not in CATEGORIES:
            flash('Invalid category.', 'error')
        elif len(description) < 10:
            flash('Description must be at least 10 characters.', 'error')
        else:
            grievances = load_grievances()
            new_grievance = {
                'id': get_next_grievance_id(),
                'student_id': session['user']['id'],
                'student_name': session['user']['name'],
                'category': category,
                'description': description,
                'status': 'Pending',
                'response': '',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': '',
                'resolved_at': ''
            }
            grievances.append(new_grievance)
            save_grievances(grievances)
            flash(f'Grievance submitted! ID: {new_grievance["id"]}', 'success')
            return redirect(url_for('student_dashboard'))
    
    return render_template('submit_grievance.html', categories=CATEGORIES, user=session['user'])


@app.route('/student/grievance/<int:gid>')
def view_grievance(gid):
    """View grievance details"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    grievances = load_grievances()
    grievance = next((g for g in grievances if g['id'] == gid), None)
    
    if not grievance:
        flash('Grievance not found.', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Check access
    if session['user']['role'] == 'student' and grievance['student_id'] != session['user']['id']:
        flash('Access denied.', 'error')
        return redirect(url_for('student_dashboard'))
    
    return render_template('view_grievance.html', grievance=grievance, user=session['user'])


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    if 'user' not in session or session['user']['role'] != 'admin':
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    grievances = load_grievances()
    
    # Filter
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    search = request.args.get('search', '').lower()
    
    if status_filter:
        grievances = [g for g in grievances if g['status'] == status_filter]
    if category_filter:
        grievances = [g for g in grievances if g['category'] == category_filter]
    if search:
        grievances = [g for g in grievances if search in g['description'].lower() or search in g['student_name'].lower()]
    
    # Stats
    all_grievances = load_grievances()
    stats = {
        'total': len(all_grievances),
        'pending': len([g for g in all_grievances if g['status'] == 'Pending']),
        'in_progress': len([g for g in all_grievances if g['status'] == 'In Progress']),
        'resolved': len([g for g in all_grievances if g['status'] == 'Resolved'])
    }
    
    return render_template('admin_dashboard.html', 
                         grievances=grievances, 
                         stats=stats, 
                         categories=CATEGORIES,
                         statuses=STATUS_OPTIONS,
                         user=session['user'])


@app.route('/admin/grievance/<int:gid>', methods=['GET', 'POST'])
def admin_view_grievance(gid):
    """Admin view/edit grievance"""
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    
    grievances = load_grievances()
    grievance = next((g for g in grievances if g['id'] == gid), None)
    
    if not grievance:
        flash('Grievance not found.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_status':
            new_status = request.form.get('status')
            if new_status in STATUS_OPTIONS:
                grievance['status'] = new_status
                grievance['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if new_status == 'Resolved':
                    grievance['resolved_at'] = grievance['updated_at']
                save_grievances(grievances)
                flash('Status updated.', 'success')
        
        elif action == 'add_response':
            response = request.form.get('response', '').strip()
            if len(response) >= 5:
                grievance['response'] = response
                grievance['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_grievances(grievances)
                flash('Response added.', 'success')
            else:
                flash('Response must be at least 5 characters.', 'error')
        
        elif action == 'delete':
            grievances = [g for g in grievances if g['id'] != gid]
            save_grievances(grievances)
            flash('Grievance deleted.', 'success')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_grievance.html', grievance=grievance, statuses=STATUS_OPTIONS, user=session['user'])


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Student Grievance Redressal System")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
