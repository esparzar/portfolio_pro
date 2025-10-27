# app/api/resources/projects.py
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.project import Project

class ProjectListResource(Resource):
    def get(self):
        projects = Project.query.filter_by(status='published').all()
        return {
            'projects': [project.to_dict() for project in projects]
        }, 200

class ProjectResource(Resource):
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)
        return project.to_dict(), 200
