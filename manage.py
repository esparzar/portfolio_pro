# manage.py
#!/usr/bin/env python
import os
from app import create_app, db
from app.models.user import User
from app.models.project import Project
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Project=Project)

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Database initialized.')

@app.cli.command()
@click.option('--username', default='admin', help='Admin username')
@click.option('--email', default='admin@portfolio.com', help='Admin email')
@click.option('--password', default='admin123', help='Admin password')
def create_admin(username, email, password):
    """Create admin user."""
    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo(f'Admin user {username} created successfully!')

if __name__ == '__main__':
    app.run()
