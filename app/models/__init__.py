from .user import User
from .contact import Contact
from .project import Project

# Define what gets exported when doing "from app.models import *"
__all__ = ['User', 'Contact', 'Project']