from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class AuthResource(Resource):
    
    def post(self):
        """Login user and return JWT token"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()
        
        try:
            user = User.authenticate(args['username'], args['password'])
            
            if not user:
                return {'error': 'Invalid credentials'}, 401
            
            if not user.is_active:
                return {'error': 'Account is disabled'}, 401
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return {'error': 'Login failed'}, 500
    
    @jwt_required()
    def get(self):
        """Get current user info"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}", exc_info=True)
            return {'error': 'Failed to get user info'}, 500
    
    @jwt_required()
    def put(self):
        """Change password"""
        parser = reqparse.RequestParser()
        parser.add_argument('current_password', type=str, required=True)
        parser.add_argument('new_password', type=str, required=True)
        args = parser.parse_args()
        
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            if not user.check_password(args['current_password']):
                return {'error': 'Current password is incorrect'}, 401
            
            user.set_password(args['new_password'])
            db.session.commit()
            
            return {'message': 'Password changed successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Password change error: {str(e)}", exc_info=True)
            return {'error': 'Failed to change password'}, 500
    
    def options(self):
        """Handle CORS preflight requests"""
        return {'allow': 'POST, GET, PUT, OPTIONS'}, 200


class RegisterResource(Resource):
    """User registration resource"""
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        
        try:
            # Check if user exists
            if User.query.filter_by(username=args['username']).first():
                return {'error': 'Username already exists'}, 400
            
            if User.query.filter_by(email=args['email']).first():
                return {'error': 'Email already exists'}, 400
            
            # Create user (not admin by default)
            user = User(
                username=args['username'],
                email=args['email'],
                is_admin=False,
                is_active=True
            )
            user.set_password(args['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return {
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return {'error': 'Registration failed'}, 500