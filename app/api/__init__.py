from flask_restful import Api

api = Api()

def initialize_api(app):
    """Attach API routes to the Flask app"""
    from app.api.routes import  register_routes
    register_routes(api)
    api.init_app(app)

