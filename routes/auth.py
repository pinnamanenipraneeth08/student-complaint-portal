"""Authentication routes"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Landing page - redirect based on login status"""
    if current_user.is_authenticated:
        if current_user.is_student:
            return redirect(url_for('student.dashboard'))
        elif current_user.is_department:
            return redirect(url_for('department.dashboard'))
        elif current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')
        
        if not user.is_active:
            flash('Your account has been deactivated. Please contact admin.', 'danger')
            return render_template('login.html')
        
        if not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')
        
        # For students, verify university email
        if user.is_student and not email.endswith(f'@{Config.UNIVERSITY_EMAIL_DOMAIN}'):
            flash(f'Students must use their {Config.UNIVERSITY_EMAIL_DOMAIN} email address.', 'danger')
            return render_template('login.html')
        
        # Login successful
        login_user(user, remember=remember)
        user.update_last_login()
        
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Redirect to appropriate dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        if user.is_student:
            return redirect(url_for('student.dashboard'))
        elif user.is_department:
            return redirect(url_for('department.dashboard'))
        elif user.is_admin:
            return redirect(url_for('admin.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        registration_number = request.form.get('registration_number', '').strip()
        room_number = request.form.get('room_number', '').strip()
        
        # Validation
        if not all([name, email, password, registration_number, room_number]):
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if not email.endswith(f'@{Config.UNIVERSITY_EMAIL_DOMAIN}'):
            flash(f'Please use your university email ({Config.UNIVERSITY_EMAIL_DOMAIN}).', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('auth.login'))
        
        if User.query.filter_by(registration_number=registration_number).first():
            flash('Registration number already in use.', 'danger')
            return render_template('register.html')
        
        # Create new student user
        user = User(
            name=name,
            email=email,
            role='student',
            registration_number=registration_number,
            room_number=room_number
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
