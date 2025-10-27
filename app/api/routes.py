# app/api/routes.py
def register_routes(api):
    # Import inside function to avoid circular imports
    from app.api.resources.auth import AuthResource
    from app.api.resources.projects import ProjectListResource, ProjectResource
    from app.api.resources.contact import ContactMessageResource
    
    # Add API routes to the api_instance
    api.add_resource(AuthResource, '/api/auth/login')
    api.add_resource(ProjectListResource, '/api/projects')
    api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
    api.add_resource(ContactMessageResource, '/api/contact')
