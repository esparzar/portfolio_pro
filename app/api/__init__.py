from flask_restful import Api

from app.api.resources.auth import AuthResource, RegisterResource
from app.api.resources.contact import ContactDetailResource, ContactResource, ContactStatsResource
from app.api.resources.projects import ProjectDetailResource, ProjectListResource


def register_api(app):
    """Register REST resources while preserving the existing API URL surface."""
    api = Api(app)
    api.add_resource(ContactResource, "/api/contacts", "/api/contacts/")
    api.add_resource(ContactDetailResource, "/api/contacts/<int:contact_id>")
    api.add_resource(ContactStatsResource, "/api/contacts/stats")
    api.add_resource(ProjectListResource, "/api/projects", "/api/projects/")
    api.add_resource(ProjectDetailResource, "/api/projects/<int:project_id>")
    api.add_resource(AuthResource, "/api/auth", "/api/auth/")
    api.add_resource(RegisterResource, "/api/auth/register", "/api/auth/register/")
    return api
