"""Complaint model"""
from datetime import datetime
from models import db
import random
import string

class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), unique=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    priority = db.Column(db.String(50), default='Medium')
    expected_resolution_date = db.Column(db.Date)
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    updates = db.relationship('ComplaintUpdate', backref='complaint', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref='complaint', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def generate_ticket_id():
        """Generate unique ticket ID"""
        while True:
            # Format: TCK-YYYYMMDD-XXXX (e.g., TCK-20250115-A1B2)
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            ticket_id = f'TCK-{date_str}-{random_str}'
            
            # Check if ticket ID already exists
            if not Complaint.query.filter_by(ticket_id=ticket_id).first():
                return ticket_id
    
    def update_status(self, new_status, user_id, message=None):
        """Update complaint status"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        if new_status == 'Completed':
            self.resolved_at = datetime.utcnow()
        
        # Create status update record
        update = ComplaintUpdate(
            complaint_id=self.id,
            user_id=user_id,
            message=message or f'Status changed from {old_status} to {new_status}',
            update_type='status_change'
        )
        db.session.add(update)
        db.session.commit()
    
    def get_status_color(self):
        """Get color class for status"""
        colors = {
            'Pending': 'warning',
            'In Progress': 'info',
            'Completed': 'success',
            'Closed': 'secondary'
        }
        return colors.get(self.status, 'secondary')
    
    def get_priority_color(self):
        """Get color class for priority"""
        colors = {
            'Low': 'success',
            'Medium': 'info',
            'High': 'warning',
            'Urgent': 'danger'
        }
        return colors.get(self.priority, 'secondary')
    
    def __repr__(self):
        return f'<Complaint {self.ticket_id}>'


class ComplaintUpdate(db.Model):
    __tablename__ = 'complaint_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    update_type = db.Column(db.String(50), default='comment')  # comment, status_change, reply
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ComplaintUpdate {self.id}>'


class Attachment(db.Model):
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attachment {self.file_name}>'
