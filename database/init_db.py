"""Database initialization script"""
import psycopg2
from psycopg2 import sql
import os
import sys

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'student_portal'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE student_portal")
            print("✅ Database 'student_portal' created successfully!")
        else:
            print("ℹ️  Database 'student_portal' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def initialize_schema():
    """Run the schema.sql file to create tables"""
    try:
        # Connect to the student_portal database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password",
            database="student_portal"
        )
        cursor = conn.cursor()
        
        # Read and execute schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Database schema initialized successfully!")
        print("✅ Default departments created")
        print("✅ Default admin user created (email: admin@klu.ac.in, password: admin123)")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error initializing schema: {e}")
        return False
    except FileNotFoundError:
        print("❌ schema.sql file not found!")
        return False

def main():
    """Main function to set up the database"""
    print("🚀 Starting database setup for Student Complaint Portal...")
    print()
    
    # Step 1: Create database
    if not create_database():
        print("❌ Database creation failed. Please check your PostgreSQL installation.")
        sys.exit(1)
    
    # Step 2: Initialize schema
    if not initialize_schema():
        print("❌ Schema initialization failed.")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✅ Database setup completed successfully!")
    print("=" * 60)
    print()
    print("Default Credentials:")
    print("  Admin Login: admin@klu.ac.in / admin123")
    print()
    print("Next Steps:")
    print("  1. Update database credentials in .env file")
    print("  2. Run: python app.py")
    print("  3. Open: http://localhost:5000")
    print()

if __name__ == "__main__":
    main()
