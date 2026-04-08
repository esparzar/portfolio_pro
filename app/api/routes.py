from flask import Blueprint
from flask_restful import Api
from app.api.resources.contact import ContactResource, ContactDetailResource
from app.api.resources.projects import ProjectResource, ProjectListResource
from app.api.resources.auth import AuthResource

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Register resources
api.add_resource(ContactResource, '/contact')
api.add_resource(ContactDetailResource, '/contact/<int:contact_id>')
api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource, '/projects/<int:project_id>')
api.add_resource(AuthResource, '/auth')