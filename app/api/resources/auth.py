from flask import request, jsonify, session
from app.models.user import User
import jwt
from datetime import datetime, timedelta
from flask import current_app

class AuthResource:
    @staticmethod
    def register(data):
        """Register new user"""
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        from app import db
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully'}), 201
    
    @staticmethod
    def login(data):
        """Login user and return token"""
        user = User.authenticate(data['username'], data['password'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200