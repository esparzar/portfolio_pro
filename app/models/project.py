from typing import Any, Self, cast

from app import db
from app.utils.datetime import utc_now


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(255), nullable=True)
    technologies = db.Column(db.String(255))
    project_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    featured_image = db.Column(db.String(255))
    images = db.Column(db.Text)
    status = db.Column(db.String(50), default="in_progress", index=True)
    featured = db.Column(db.Boolean, default=False, index=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    display_order = db.Column(db.Integer, default=0, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationship
    # user = db.relationship("User", backref="projects")

    @classmethod
    def get_all_active(cls) -> list[Self]:
        return cast(
            list[Self], cls.query.order_by(cls.display_order.asc(), cls.created_at.desc()).all()
        )

    @classmethod
    def get_featured(cls) -> list[Self]:
        return cast(
            list[Self], cls.query.filter_by(featured=True).order_by(cls.display_order).all()
        )

    def get_technologies_list(self) -> list[str]:
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(",")]
        return []

    def __repr__(self) -> str:
        return f"<Project {self.title}>"

    def to_dict(self) -> dict[str, Any]:
        """Convert project to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "short_description": self.short_description,
            "technologies": self.technologies,
            "project_url": self.project_url,
            "github_url": self.github_url,
            "featured_image": self.featured_image,
            "images": self.images,
            "status": self.status,
            "featured": self.featured,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
