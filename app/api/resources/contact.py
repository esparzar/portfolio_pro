from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models.contact import Contact
from app.services.email_service import send_email

class ContactResource(Resource):
    """Contact form API resource"""
    
    def post(self):
        """Submit contact form"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data:
                return {'error': f'{field} is required'}, 400
        
        # Save to database
        contact = Contact(
            name=data['name'],
            email=data['email'],
            service=data.get('service', ''),
            message=data['message'],
            ip_address=request.remote_addr
        )
        contact.save()
        
        # Send notification email
        try:
            send_email(
                subject=f"New Contact: {data['name']}",
                recipients=[current_app.config['ADMIN_EMAIL']],
                body=f"Message from {data['name']} ({data['email']}):\n\n{data['message']}"
            )
        except Exception as e:
            current_app.logger.error(f"Email error: {str(e)}")
        
        return {'message': 'Message sent successfully'}, 201
    
    @jwt_required()
    def get(self):
        """Get all contacts (admin only)"""
        contacts = Contact.get_all()
        return {
            'contacts': [contact.to_dict() for contact in contacts],
            'count': len(contacts)
        }, 200

class ContactDetailResource(Resource):
    """Single contact API resource"""
    
    @jwt_required()
    def get(self, contact_id):
        """Get specific contact"""
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'error': 'Contact not found'}, 404
        return contact.to_dict(), 200
    
    @jwt_required()
    def put(self, contact_id):
        """Mark contact as read"""
        if Contact.mark_as_read(contact_id):
            return {'message': 'Contact marked as read'}, 200
        return {'error': 'Contact not found'}, 404