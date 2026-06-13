from .auth import AuthResource, RegisterResource
from .contact import ContactDetailResource, ContactResource, ContactStatsResource
from .projects import ProjectDetailResource, ProjectListResource

__all__ = [
    "ContactResource",
    "ContactDetailResource",
    "ContactStatsResource",
    "ProjectListResource",
    "ProjectDetailResource",
    "AuthResource",
    "RegisterResource",
]
