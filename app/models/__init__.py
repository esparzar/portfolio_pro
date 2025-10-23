# app/models/__init__.py
from .user import User
from .project import Project
from .contact import ContactMessage

__all__ = ['User', 'Project', 'ContactMessage']
