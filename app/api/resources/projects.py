from flask import jsonify
from app.models.project import Project

class ProjectResource:
    @staticmethod
    def get_all():
        """Get all projects"""
        projects = Project.get_all_active()
        return jsonify({
            'projects': [project.to_dict() for project in projects],
            'count': len(projects)
        })
    
    @staticmethod
    def get_one(project_id):
        """Get single project by ID"""
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(project.to_dict())