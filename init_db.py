"""SQLite Database initialization script"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.user import User
from models.department import Department
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and default data"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Creating database tables...")
        
        # Create all tables
        db.create_all()
        print("✅ Tables created successfully!")
        
        # Check if departments already exist
        if Department.query.first():
            print("ℹ️  Database already initialized with data")
            return
        
        # Insert default departments
        departments = [
            Department(name='Food', email='food@klu.ac.in', 
                      description='Handles all food and mess related complaints'),
            Department(name='Cleaning', email='cleaning@klu.ac.in',
                      description='Handles cleaning and sanitation issues'),
            Department(name='Electrical', email='electrical@klu.ac.in',
                      description='Handles electrical repairs and maintenance'),
            Department(name='Plumbing', email='plumbing@klu.ac.in',
                      description='Handles plumbing and water supply issues'),
            Department(name='Carpentry', email='carpentry@klu.ac.in',
                      description='Handles furniture and carpentry work')
        ]
        
        for dept in departments:
            db.session.add(dept)
        
        db.session.commit()
        print("✅ Default departments created")
        
        # Insert default admin user
        admin = User(
            name='Admin User',
            email='admin@klu.ac.in',
            role='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Default admin user created")
        print()
        print("=" * 60)
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print()
        print("Default Credentials:")
        print("  Admin Login: admin@klu.ac.in / admin123")
        print()
        print("Next Steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print()

if __name__ == "__main__":
    init_database()
