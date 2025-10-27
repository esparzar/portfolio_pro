# app/api/resources/__init__.py
from .auth import AuthResource
from .projects import ProjectListResource, ProjectResource
from .contact import ContactMessageResource

__all__ = [
    'AuthResource',
    'ProjectListResource', 
    'ProjectResource',
    'ContactMessageResource'
]
