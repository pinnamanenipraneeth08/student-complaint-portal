"""Admin routes"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.complaint import Complaint
from models.department import Department
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin():
    """Ensure only admins can access these routes"""
    if not current_user.is_authenticated:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('auth.login'))
    
    if not current_user.is_admin:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.index'))

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard - overview of all complaints"""
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    department_filter = request.args.get('department', 'all')
    
    # Base query
    query = Complaint.query
    
    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if department_filter != 'all':
        query = query.filter_by(department_id=int(department_filter))
    
    # Get complaints
    complaints = query.order_by(Complaint.created_at.desc()).limit(50).all()
    
    # Overall statistics
    total_complaints = Complaint.query.count()
    pending = Complaint.query.filter_by(status='Pending').count()
    in_progress = Complaint.query.filter_by(status='In Progress').count()
    completed = Complaint.query.filter_by(status='Completed').count()
    
    # Department-wise statistics
    dept_stats = db.session.query(
        Department.name,
        func.count(Complaint.id).label('total'),
        func.sum(db.case((Complaint.status == 'Pending', 1), else_=0)).label('pending'),
        func.sum(db.case((Complaint.status == 'Completed', 1), else_=0)).label('completed')
    ).join(Complaint).group_by(Department.name).all()
    
    # Get long-pending complaints (pending for more than 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    long_pending = Complaint.query.filter(
        Complaint.status == 'Pending',
        Complaint.created_at < seven_days_ago
    ).order_by(Complaint.created_at).all()
    
    departments = Department.get_all()
    
    return render_template('admin/dashboard.html',
                         complaints=complaints,
                         total_complaints=total_complaints,
                         pending=pending,
                         in_progress=in_progress,
                         completed=completed,
                         dept_stats=dept_stats,
                         long_pending=long_pending,
                         departments=departments,
                         status_filter=status_filter,
                         department_filter=department_filter)

@admin_bp.route('/complaint/<ticket_id>')
def view_complaint(ticket_id):
    """View complaint details"""
    complaint = Complaint.query.filter_by(ticket_id=ticket_id).first_or_404()
    return render_template('admin/view_complaint.html', complaint=complaint)

@admin_bp.route('/users')
def users():
    """Manage users"""
    role_filter = request.args.get('role', 'all')
    
    query = User.query
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    users = query.order_by(User.created_at.desc()).all()
    
    # Statistics
    total_users = User.query.count()
    students = User.query.filter_by(role='student').count()
    department_users = User.query.filter(User.role.in_(['department', 'warden'])).count()
    
    return render_template('admin/users.html',
                         users=users,
                         total_users=total_users,
                         students=students,
                         department_users=department_users,
                         role_filter=role_filter)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create new department/warden user"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'department')
        department_id = request.form.get('department_id')
        
        # Validation
        if not all([name, email, password, department_id]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        if role not in ['department', 'warden']:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Create user
        user = User(
            name=name,
            email=email,
            role=role,
            department_id=int(department_id)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'{role.title()} user created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    departments = Department.get_all()
    return render_template('admin/create_user.html', departments=departments)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
def toggle_user_status(user_id):
    """Activate/deactivate user"""
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cannot deactivate admin users.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {status} successfully.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/reports')
def reports():
    """View reports and analytics"""
    # Time-based statistics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    recent_complaints = Complaint.query.filter(Complaint.created_at >= thirty_days_ago).count()
    recent_completed = Complaint.query.filter(
        Complaint.created_at >= thirty_days_ago,
        Complaint.status == 'Completed'
    ).count()
    
    # Average resolution time (for completed complaints)
    completed = Complaint.query.filter(
        Complaint.status == 'Completed',
        Complaint.resolved_at.isnot(None)
    ).all()
    
    avg_resolution_hours = 0
    if completed:
        total_hours = sum([
            (c.resolved_at - c.created_at).total_seconds() / 3600
            for c in completed
        ])
        avg_resolution_hours = round(total_hours / len(completed), 1)
    
    # Priority distribution
    priority_stats = db.session.query(
        Complaint.priority,
        func.count(Complaint.id).label('count')
    ).group_by(Complaint.priority).all()
    
    return render_template('admin/reports.html',
                         recent_complaints=recent_complaints,
                         recent_completed=recent_completed,
                         avg_resolution_hours=avg_resolution_hours,
                         priority_stats=priority_stats)
