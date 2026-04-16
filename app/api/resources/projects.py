from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.project import Project
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class ProjectResource(Resource):
    def get(self, project_id=None):
        """Get projects - all if no ID, single if ID provided"""
        try:
            if project_id:
                # Get single project
                project = Project.query.get(project_id)
                if not project:
                    return {'error': 'Project not found'}, 404
                return {'project': project.to_dict()}, 200
            else:
                # Get all projects
                featured_only = request.args.get('featured', 'false').lower() == 'true'
                
                if featured_only:
                    projects = Project.get_featured()
                else:
                    projects = Project.get_all_active()
                
                return {
                    'projects': [project.to_dict() for project in projects],
                    'count': len(projects)
                }, 200
                
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}", exc_info=True)
            return {'error': 'Failed to retrieve projects'}, 500
    
    @jwt_required()
    def post(self):
        """Create a new project (admin only)"""
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'error': 'Admin access required'}, 403
            
            data = request.get_json()
            
            if not data or not data.get('title'):
                return {'error': 'Title is required'}, 400
            
            project = Project(
                title=data.get('title'),
                description=data.get('description', ''),
                short_description=data.get('short_description', ''),
                technologies=data.get('technologies', ''),
                github_url=data.get('github_url', ''),
                project_url=data.get('project_url', ''),
                featured_image=data.get('featured_image', ''),
                featured=data.get('featured', False),
                status=data.get('status', 'completed'),
                display_order=data.get('display_order', 0)
            )
            
            db.session.add(project)
            db.session.commit()
            
            logger.info(f"Project created: {project.title} by admin {user.username}")
            
            return {
                'message': 'Project created successfully',
                'project': project.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating project: {str(e)}", exc_info=True)
            return {'error': 'Failed to create project'}, 500


class ProjectListResource(Resource):
    """Resource for listing all projects"""
    
    def get(self):
        """Get all projects"""
        try:
            featured_only = request.args.get('featured', 'false').lower() == 'true'
            
            if featured_only:
                projects = Project.get_featured()
            else:
                projects = Project.get_all_active()
            
            return {
                'projects': [project.to_dict() for project in projects],
                'count': len(projects)
            }, 200
            
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}", exc_info=True)
            return {'error': 'Failed to retrieve projects'}, 500


class ProjectDetailResource(Resource):
    """Resource for single project operations"""
    
    def get(self, project_id):
        """Get a single project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {'error': 'Project not found'}, 404
            return {'project': project.to_dict()}, 200
            
        except Exception as e:
            logger.error(f"Error getting project: {str(e)}", exc_info=True)
            return {'error': 'Failed to retrieve project'}, 500
    
    @jwt_required()
    def put(self, project_id):
        """Update a project"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'error': 'Admin access required'}, 403
            
            project = Project.query.get(project_id)
            if not project:
                return {'error': 'Project not found'}, 404
            
            data = request.get_json()
            
            if 'title' in data:
                project.title = data['title']
            if 'description' in data:
                project.description = data['description']
            if 'short_description' in data:
                project.short_description = data['short_description']
            if 'technologies' in data:
                project.technologies = data['technologies']
            if 'github_url' in data:
                project.github_url = data['github_url']
            if 'project_url' in data:
                project.project_url = data['project_url']
            if 'featured_image' in data:
                project.featured_image = data['featured_image']
            if 'featured' in data:
                project.featured = data['featured']
            if 'status' in data:
                project.status = data['status']
            if 'display_order' in data:
                project.display_order = data['display_order']
            
            db.session.commit()
            
            return {
                'message': 'Project updated successfully',
                'project': project.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating project: {str(e)}", exc_info=True)
            return {'error': 'Failed to update project'}, 500
    
    @jwt_required()
    def delete(self, project_id):
        """Delete a project"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'error': 'Admin access required'}, 403
            
            project = Project.query.get(project_id)
            if not project:
                return {'error': 'Project not found'}, 404
            
            db.session.delete(project)
            db.session.commit()
            
            logger.info(f"Project deleted: {project.title} by admin {user.username}")
            
            return {'message': 'Project deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting project: {str(e)}", exc_info=True)
            return {'error': 'Failed to delete project'}, 500