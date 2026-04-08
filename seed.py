#!/usr/bin/env python
"""Simple script to create admin user"""
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True,
            is_active=True
        )
        # Change 'your-password-here' to a secure password
        admin.set_password('your-password-here')
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
        print("   Username: admin")
        print("   Password: your-password-here")
    else:
        print("✅ Admin user already exists")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")

# List all users
print("\n📋 All users in database:")
users = User.query.all()
for user in users:
    print(f"   - {user.username} (Admin: {user.is_admin})")