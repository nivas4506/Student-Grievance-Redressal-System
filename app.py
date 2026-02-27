"""
Student Grievance Redressal System - Web Version
Flask web application with OOP classes, CSV+JSON storage, and Analytics

Demonstrates:
- Flask web framework (routes, templates, sessions)
- OOP classes (Student, Grievance, Admin from models.py)
- Dual storage (JSON + CSV via file_handler.py)
- Analytics with Pandas (via analytics.py)
- Matplotlib chart generation
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from datetime import datetime
import os

from file_handler import (
    initialize_data_files, load_users, save_users,
    load_grievances, save_grievances,
    get_next_user_id, get_next_grievance_id
)
from auth import hash_password, validate_email, email_exists
from models import Student, Grievance, Admin
from analytics.analyzer import GrievanceAnalyzer, PANDAS_AVAILABLE
from analytics.visualization import GrievanceVisualizer, MATPLOTLIB_AVAILABLE

app = Flask(__name__)
app.secret_key = 'grievance_system_secret_key_2026'

# Categories and Status options (from Grievance OOP class)
CATEGORIES = Grievance.CATEGORIES
STATUS_OPTIONS = Grievance.STATUS_OPTIONS

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
            # Create Student object using OOP class
            user_id = get_next_user_id()
            student_obj = Student(
                student_id=user_id,
                name=name,
                email=email,
                password=hash_password(password),
                dept=request.form.get('dept', 'General')
            )
            
            users = load_users()
            user_dict = student_obj.to_dict()
            user_dict['created_at'] = str(datetime.now().date())
            users.append(user_dict)
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
            # Create Grievance object using OOP class
            grievance_obj = Grievance(
                grievance_id=get_next_grievance_id(),
                student_id=session['user']['id'],
                student_name=session['user']['name'],
                category=category,
                description=description
            )
            
            grievances = load_grievances()
            grievances.append(grievance_obj.to_dict())
            save_grievances(grievances)
            flash(f'Grievance submitted! ID: {grievance_obj.grievance_id}', 'success')
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
            # Use OOP Grievance class for status update
            grievance_obj = Grievance.from_dict(grievance)
            success, message = grievance_obj.update_status(new_status)
            if success:
                # Update the dict in list
                for i, g in enumerate(grievances):
                    if g['id'] == gid:
                        grievances[i] = grievance_obj.to_dict()
                        break
                save_grievances(grievances)
                flash('Status updated.', 'success')
                # Reload for display
                grievance = grievance_obj.to_dict()
            else:
                flash(message, 'error')
        
        elif action == 'add_response':
            response = request.form.get('response', '').strip()
            # Use OOP Grievance class for adding response
            grievance_obj = Grievance.from_dict(grievance)
            success, message = grievance_obj.add_response(response)
            if success:
                for i, g in enumerate(grievances):
                    if g['id'] == gid:
                        grievances[i] = grievance_obj.to_dict()
                        break
                save_grievances(grievances)
                flash('Response added.', 'success')
                grievance = grievance_obj.to_dict()
            else:
                flash(message, 'error')
        
        elif action == 'delete':
            grievances = [g for g in grievances if g['id'] != gid]
            save_grievances(grievances)
            flash('Grievance deleted.', 'success')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_grievance.html', grievance=grievance, statuses=STATUS_OPTIONS, user=session['user'])


# ==================== ANALYTICS ROUTES ====================

@app.route('/admin/analytics')
def admin_analytics():
    """Analytics dashboard with Pandas data and Matplotlib charts"""
    if 'user' not in session or session['user']['role'] != 'admin':
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    # Get analytics data using Pandas (OOP GrievanceAnalyzer class)
    analyzer = GrievanceAnalyzer()
    summary = analyzer.get_summary_statistics()
    
    resolution_stats = {
        'total': summary['total_grievances'],
        'pending': summary['pending_count'],
        'in_progress': summary['status_breakdown'].get('In Progress', 0),
        'resolved': summary['status_breakdown'].get('Resolved', 0),
        'rejected': summary['status_breakdown'].get('Rejected', 0),
        'resolution_rate': summary['resolution_rate']
    }
    category_data = summary['category_breakdown']
    status_data = summary['status_breakdown']
    monthly_data = summary['monthly_trend']
    
    # Generate charts using Matplotlib (OOP GrievanceVisualizer class)
    charts = {}
    if MATPLOTLIB_AVAILABLE:
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        visualizer = GrievanceVisualizer(analyzer)
        visualizer.output_dir = static_dir
        
        path = visualizer.create_category_bar_chart(save=True, show=False)
        if path:
            charts['category'] = os.path.basename(path)
        
        path = visualizer.create_status_pie_chart(save=True, show=False)
        if path:
            charts['status'] = os.path.basename(path)
        
        path = visualizer.create_monthly_trend_line(save=True, show=False)
        if path:
            charts['trend'] = os.path.basename(path)
    
    return render_template('analytics.html',
                         resolution_stats=resolution_stats,
                         category_data=category_data,
                         status_data=status_data,
                         monthly_data=monthly_data,
                         charts=charts,
                         pandas_available=PANDAS_AVAILABLE,
                         matplotlib_available=MATPLOTLIB_AVAILABLE,
                         user=session['user'])


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Student Grievance Redressal System")
    print("  Open http://127.0.0.1:5000 in your browser")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
