"""Department model"""
from datetime import datetime
from models import db

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    complaints = db.relationship('Complaint', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'
    
    @staticmethod
    def get_all():
        """Get all departments"""
        return Department.query.order_by(Department.name).all()
    
    @staticmethod
    def get_by_name(name):
        """Get department by name"""
        return Department.query.filter_by(name=name).first()
