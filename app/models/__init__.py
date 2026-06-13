from .contact import Contact
from .project import Project
from .user import User

# Define what gets exported when doing "from app.models import *"
__all__ = ["User", "Contact", "Project"]
