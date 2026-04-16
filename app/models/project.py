from datetime import datetime
from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(255), nullable=True)
    technologies = db.Column(db.String(255))
    project_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    featured_image = db.Column(db.String(255))
    images = db.Column(db.Text)
    status = db.Column(db.String(50), default="in_progress")
    featured = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    display_order = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationship
    #user = db.relationship("User", backref="projects")
    
    @classmethod
    def get_all_active(cls):
        return cls.query.order_by(cls.display_order.asc(), cls.created_at.desc()).all()
    
    @classmethod
    def get_featured(cls):
        return cls.query.filter_by(featured=True).order_by(cls.display_order).all()
    
    def get_technologies_list(self):
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []
    
    def __repr__(self):
        return f"<Project {self.title}>"