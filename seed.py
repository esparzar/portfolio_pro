#!/usr/bin/env python
"""Create admin user and optional demo project with static screenshots."""
import json

from app import create_app, db
from app.models.user import User
from app.models.project import Project

app = create_app()

PORTFOLIO_GALLERY_PATHS = [
    "project/projects-section.png",
    "project/admin-dashboard.png",
    "project/project-detail.png",
    "project/mobile-view.png",
    "project/project-gallary.png",
]


def seed_demo_portfolio_project():
    if Project.query.count() > 0:
        return
    project = Project(
        title="Portfolio Pro",
        description=(
            "Full-stack developer portfolio built with Flask: public site, admin CMS, "
            "REST API, contact flow, and PostgreSQL-ready deployment."
        ),
        short_description="Production-ready portfolio with admin dashboard and API.",
        technologies="Python, Flask, SQLAlchemy, PostgreSQL, Bootstrap",
        featured_image="project/homepage-hero.png",
        images=json.dumps(PORTFOLIO_GALLERY_PATHS),
        featured=True,
        status="completed",
        display_order=0,
    )
    db.session.add(project)
    db.session.commit()
    print("✅ Demo project seeded (featured_image + gallery use static PNGs under images/project/).")


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

    seed_demo_portfolio_project()

# List all users
print("\n📋 All users in database:")
users = User.query.all()
for user in users:
    print(f"   - {user.username} (Admin: {user.is_admin})")