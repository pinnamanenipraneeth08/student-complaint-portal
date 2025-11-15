"""Department/Warden routes"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.complaint import Complaint, ComplaintUpdate
from models.user import User
from datetime import datetime, date

department_bp = Blueprint('department', __name__, url_prefix='/department')

@department_bp.before_request
def check_department():
    """Ensure only department users can access these routes"""
    if not current_user.is_authenticated:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('auth.login'))
    
    if not current_user.is_department:
        flash('Access denied. Department users only.', 'danger')
        return redirect(url_for('auth.index'))

@department_bp.route('/dashboard')
def dashboard():
    """Department dashboard - view complaints for their department"""
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    # Base query - only complaints for this department
    query = Complaint.query.filter_by(department_id=current_user.department_id)
    
    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    
    # Get complaints ordered by newest first
    complaints = query.order_by(Complaint.created_at.desc()).all()
    
    # Get statistics
    total_complaints = Complaint.query.filter_by(department_id=current_user.department_id).count()
    pending = Complaint.query.filter_by(department_id=current_user.department_id, status='Pending').count()
    in_progress = Complaint.query.filter_by(department_id=current_user.department_id, status='In Progress').count()
    completed = Complaint.query.filter_by(department_id=current_user.department_id, status='Completed').count()
    
    return render_template('department/dashboard.html',
                         complaints=complaints,
                         total_complaints=total_complaints,
                         pending=pending,
                         in_progress=in_progress,
                         completed=completed,
                         status_filter=status_filter,
                         priority_filter=priority_filter)

@department_bp.route('/complaint/<ticket_id>')
def view_complaint(ticket_id):
    """View complaint details"""
    complaint = Complaint.query.filter_by(
        ticket_id=ticket_id,
        department_id=current_user.department_id
    ).first_or_404()
    
    return render_template('department/view_complaint.html', complaint=complaint)

@department_bp.route('/complaint/<ticket_id>/reply', methods=['POST'])
def reply_complaint(ticket_id):
    """Reply to a complaint"""
    complaint = Complaint.query.filter_by(
        ticket_id=ticket_id,
        department_id=current_user.department_id
    ).first_or_404()
    
    message = request.form.get('message', '').strip()
    if not message:
        flash('Please enter a message.', 'danger')
        return redirect(url_for('department.view_complaint', ticket_id=ticket_id))
    
    # Create reply
    update = ComplaintUpdate(
        complaint_id=complaint.id,
        user_id=current_user.id,
        message=message,
        update_type='reply'
    )
    db.session.add(update)
    complaint.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Reply sent successfully.', 'success')
    return redirect(url_for('department.view_complaint', ticket_id=ticket_id))

@department_bp.route('/complaint/<ticket_id>/update-status', methods=['POST'])
def update_status(ticket_id):
    """Update complaint status"""
    complaint = Complaint.query.filter_by(
        ticket_id=ticket_id,
        department_id=current_user.department_id
    ).first_or_404()
    
    new_status = request.form.get('status')
    message = request.form.get('message', '').strip()
    expected_date = request.form.get('expected_resolution_date')
    
    if not new_status:
        flash('Please select a status.', 'danger')
        return redirect(url_for('department.view_complaint', ticket_id=ticket_id))
    
    # Update expected resolution date if provided
    if expected_date:
        try:
            complaint.expected_resolution_date = datetime.strptime(expected_date, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Update status
    status_message = message or f'Status updated to {new_status}'
    complaint.update_status(new_status, current_user.id, status_message)
    
    flash(f'Status updated to {new_status} successfully.', 'success')
    return redirect(url_for('department.view_complaint', ticket_id=ticket_id))

@department_bp.route('/complaint/<ticket_id>/set-priority', methods=['POST'])
def set_priority(ticket_id):
    """Set complaint priority"""
    complaint = Complaint.query.filter_by(
        ticket_id=ticket_id,
        department_id=current_user.department_id
    ).first_or_404()
    
    priority = request.form.get('priority')
    if priority in ['Low', 'Medium', 'High', 'Urgent']:
        old_priority = complaint.priority
        complaint.priority = priority
        complaint.updated_at = datetime.utcnow()
        
        # Create update record
        update = ComplaintUpdate(
            complaint_id=complaint.id,
            user_id=current_user.id,
            message=f'Priority changed from {old_priority} to {priority}',
            update_type='status_change'
        )
        db.session.add(update)
        db.session.commit()
        
        flash(f'Priority updated to {priority}.', 'success')
    else:
        flash('Invalid priority level.', 'danger')
    
    return redirect(url_for('department.view_complaint', ticket_id=ticket_id))
