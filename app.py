"""Main Flask application"""
from flask import Flask, render_template
from config import Config
from models import db, login_manager, init_app as init_models
import os

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_models(app)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.department import department_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processor for templates
    @app.context_processor
    def utility_processor():
        return {
            'now': lambda: __import__('datetime').datetime.utcnow()
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("🎓 Student Complaint Portal")
    print("=" * 60)
    print(f"🌐 Server running at: http://localhost:5000")
    print(f"📧 Default Admin: admin@klu.ac.in / admin123")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
