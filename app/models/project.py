# app/models/project.py
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    technologies = db.Column(db.String(300))  # Comma-separated list
    project_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    featured_image = db.Column(db.String(500))
    images = db.Column(JSON)  # JSON array of image paths
    status = db.Column(db.String(20), default='published')  # draft, published, archived
    featured = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    display_order = db.Column(db.Integer, default=0)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.short_description,
            'technologies': self.technologies.split(',') if self.technologies else [],
            'project_url': self.project_url,
            'github_url': self.github_url,
            'featured_image': self.featured_image,
            'images': self.images or [],
            'status': self.status,
            'featured': self.featured,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'display_order': self.display_order,
            'author': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Project {self.title}>'
