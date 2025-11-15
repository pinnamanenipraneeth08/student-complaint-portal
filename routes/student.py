"""Student routes"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db
from models.complaint import Complaint, ComplaintUpdate, Attachment
from models.department import Department
from config import Config
import os
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@student_bp.before_request
def check_student():
    """Ensure only students can access these routes"""
    if not current_user.is_authenticated:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('auth.login'))
    
    if not current_user.is_student:
        flash('Access denied. Students only.', 'danger')
        return redirect(url_for('auth.index'))

@student_bp.route('/dashboard')
def dashboard():
    """Student dashboard - view all complaints"""
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    department_filter = request.args.get('department', 'all')
    
    # Base query
    query = Complaint.query.filter_by(student_id=current_user.id)
    
    # Apply filters
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if department_filter != 'all':
        query = query.filter_by(department_id=int(department_filter))
    
    # Get complaints ordered by newest first
    complaints = query.order_by(Complaint.created_at.desc()).all()
    
    # Get statistics
    total_complaints = Complaint.query.filter_by(student_id=current_user.id).count()
    pending = Complaint.query.filter_by(student_id=current_user.id, status='Pending').count()
    in_progress = Complaint.query.filter_by(student_id=current_user.id, status='In Progress').count()
    completed = Complaint.query.filter_by(student_id=current_user.id, status='Completed').count()
    
    # Get all departments for filter
    departments = Department.get_all()
    
    return render_template('student/dashboard.html',
                         complaints=complaints,
                         total_complaints=total_complaints,
                         pending=pending,
                         in_progress=in_progress,
                         completed=completed,
                         departments=departments,
                         status_filter=status_filter,
                         department_filter=department_filter)

@student_bp.route('/submit-complaint', methods=['GET', 'POST'])
def submit_complaint():
    """Submit a new complaint"""
    if request.method == 'POST':
        department_id = request.form.get('department_id')
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'Medium')
        
        # Validation
        if not all([department_id, subject, description]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('student.submit_complaint'))
        
        # Create complaint
        complaint = Complaint(
            ticket_id=Complaint.generate_ticket_id(),
            student_id=current_user.id,
            department_id=int(department_id),
            subject=subject,
            description=description,
            priority=priority,
            status='Pending'
        )
        
        db.session.add(complaint)
        db.session.flush()  # Get the complaint ID
        
        # Handle file uploads
        files = request.files.getlist('attachments')
        if files:
            # Create upload directory if it doesn't exist
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{complaint.ticket_id}_{timestamp}_{filename}"
                    filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
                    
                    file.save(filepath)
                    
                    # Create attachment record
                    attachment = Attachment(
                        complaint_id=complaint.id,
                        file_name=filename,
                        file_path=unique_filename,
                        file_type=filename.rsplit('.', 1)[1].lower(),
                        file_size=os.path.getsize(filepath)
                    )
                    db.session.add(attachment)
        
        db.session.commit()
        
        flash(f'Complaint submitted successfully! Your ticket ID is: {complaint.ticket_id}', 'success')
        return redirect(url_for('student.view_complaint', ticket_id=complaint.ticket_id))
    
    # GET request
    departments = Department.get_all()
    return render_template('student/submit_complaint.html', departments=departments)

@student_bp.route('/complaint/<ticket_id>')
def view_complaint(ticket_id):
    """View complaint details"""
    complaint = Complaint.query.filter_by(ticket_id=ticket_id, student_id=current_user.id).first_or_404()
    return render_template('student/view_complaint.html', complaint=complaint)

@student_bp.route('/complaint/<ticket_id>/reply', methods=['POST'])
def reply_complaint(ticket_id):
    """Add a reply to complaint"""
    complaint = Complaint.query.filter_by(ticket_id=ticket_id, student_id=current_user.id).first_or_404()
    
    message = request.form.get('message', '').strip()
    if not message:
        flash('Please enter a message.', 'danger')
        return redirect(url_for('student.view_complaint', ticket_id=ticket_id))
    
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
    
    flash('Reply added successfully.', 'success')
    return redirect(url_for('student.view_complaint', ticket_id=ticket_id))
