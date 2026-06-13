#!/usr/bin/env python
"""Seed optional demo project data and create an admin only when configured."""
import json
import os

from app import create_app, db
from app.models.project import Project
from app.models.user import User

app = create_app(os.getenv("FLASK_CONFIG") or "development")

PORTFOLIO_GALLERY_PATHS = [
    "project/projects-section.png",
    "project/admin-dashboard.png",
    "project/project-detail.png",
    "project/mobile-view.png",
    "project/project-gallary.png",
]


def seed_admin_user():
    username = os.getenv("ADMIN_USERNAME", "admin")
    email = os.getenv("ADMIN_USER_EMAIL", "admin@example.com")
    password = os.getenv("ADMIN_PASSWORD")

    admin = User.query.filter_by(username=username).first()
    if admin:
        print(f"Admin user already exists: {admin.username}")
        return

    if not password:
        print("Skipping admin creation. Set ADMIN_PASSWORD to seed an admin user.")
        return

    admin = User(username=username, email=email, is_admin=True, is_active=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user created: {username}")


def seed_demo_portfolio_project():
    if Project.query.count() > 0:
        print("Project data already exists. Skipping demo project.")
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
    print("Demo project seeded.")


with app.app_context():
    seed_admin_user()
    seed_demo_portfolio_project()
