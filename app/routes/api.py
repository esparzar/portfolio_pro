from flask import Blueprint, request, jsonify
from app.api.resources.contact import ContactResource
from app.api.resources.projects import ProjectResource
from app.api.resources.auth import AuthResource

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/contact', methods=['POST'])
def api_contact():
    """API endpoint for contact form"""
    data = request.json
    return ContactResource.submit(data)

@api_bp.route('/projects', methods=['GET'])
def api_projects():
    """API endpoint to get projects"""
    return ProjectResource.get_all()

@api_bp.route('/projects/<int:project_id>', methods=['GET'])
def api_project(project_id):
    """API endpoint to get single project"""
    return ProjectResource.get_one(project_id)

@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """API endpoint for user registration"""
    data = request.json
    return AuthResource.register(data)

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API endpoint for user login"""
    data = request.json
    return AuthResource.login(data)