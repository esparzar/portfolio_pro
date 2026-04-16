from flask_restful import Resource, reqparse
from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import db, limiter
from app.models.contact import Contact
from app.models.user import User
from app.services.email_service import send_contact_notification
import logging
import re

# Get logger
logger = logging.getLogger(__name__)

class ContactResource(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('service', type=str, required=False, default='General Inquiry')
        self.parser.add_argument('message', type=str, required=True, help='Message is required')
        super().__init__()
    
    def _validate_email(self, email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    def _validate_name(self, name):
        """Validate name (minimum 2 characters, letters and spaces only)"""
        return len(name.strip()) >= 2 and all(c.isalpha() or c.isspace() for c in name)
    
    def _sanitize_input(self, text):
        """Basic sanitization to prevent XSS"""
        if not text:
            return text
        # Remove HTML tags
        import re
        return re.sub(r'<[^>]*>', '', text)
    
    @limiter.limit("5 per hour")
    def post(self):
        """Submit contact form with rate limiting (max 5 per hour)"""
        # Get client IP for logging
        client_ip = request.remote_addr
        
        try:
            args = self.parser.parse_args()
            
            # Sanitize inputs
            name = self._sanitize_input(args['name'])[:100]
            email = self._sanitize_input(args['email'])[:120]
            service = self._sanitize_input(args['service'])[:50]
            message = self._sanitize_input(args['message'])[:1000]
            
            # Validate inputs
            if not self._validate_name(name):
                return {
                    'success': False,
                    'message': 'Invalid name format. Use at least 2 letters.'
                }, 400
            
            if not self._validate_email(email):
                return {
                    'success': False,
                    'message': 'Invalid email format. Example: name@domain.com'
                }, 400
            
            if len(message) < 10:
                return {
                    'success': False,
                    'message': 'Message must be at least 10 characters'
                }, 400
            
            # Check for duplicate submissions (same email + message within 5 minutes)
            from datetime import datetime, timedelta
            five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
            duplicate = Contact.query.filter(
                Contact.email == email,
                Contact.message == message,
                Contact.created_at >= five_minutes_ago
            ).first()
            
            if duplicate:
                logger.warning(f"Duplicate contact submission from {email}")
                return {
                    'success': False,
                    'message': 'You recently submitted a similar message. Please wait before sending another.'
                }, 429
            
            # Create contact
            contact = Contact(
                name=name,
                email=email,
                service=service,
                message=message,
                ip_address=client_ip,
                user_agent=str(request.user_agent)
            )
            
            db.session.add(contact)
            db.session.commit()
            
            logger.info(f"New contact message from {name} ({email})")
            
            # Send notification email
            try:
                send_contact_notification(contact)
            except Exception as e:
                logger.error(f"Failed to send notification email: {str(e)}")
                # Don't fail the request if email fails
            
            return {
                'success': True,
                'message': 'Message sent successfully! I will get back to you within 24 hours.',
                'contact_id': contact.id
            }, 201
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating contact: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': 'Failed to submit contact form. Please try again later.'
            }, 500
    
    @jwt_required()
    def get(self):
        """Get recent contacts (admin only)"""
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {
                    'success': False,
                    'message': 'Admin access required'
                }, 403
            
            # Get query parameters
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            unread_only = request.args.get('unread', 'false').lower() == 'true'
            
            # Build query
            query = Contact.query.order_by(Contact.created_at.desc())
            
            if unread_only:
                query = query.filter_by(is_read=False)
            
            contacts = query.offset(offset).limit(limit).all()
            total = query.count()
            
            return {
                'success': True,
                'contacts': [c.to_dict() for c in contacts],
                'total': total,
                'limit': limit,
                'offset': offset
            }, 200
            
        except Exception as e:
            logger.error(f"Error retrieving contacts: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': 'Failed to retrieve contacts'
            }, 500

class ContactDetailResource(Resource):
    
    @jwt_required()
    def get(self, contact_id):
        """Get a specific contact by ID (admin only)"""
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'success': False, 'message': 'Admin access required'}, 403
            
            contact = Contact.query.get(contact_id)
            
            if not contact:
                return {'success': False, 'message': 'Contact not found'}, 404
            
            # Mark as read when viewed
            if not contact.is_read:
                contact.is_read = True
                db.session.commit()
            
            return {
                'success': True,
                'contact': contact.to_dict()
            }, 200
            
        except Exception as e:
            logger.error(f"Error retrieving contact {contact_id}: {str(e)}", exc_info=True)
            return {'success': False, 'message': 'Failed to retrieve contact'}, 500
    
    @jwt_required()
    def delete(self, contact_id):
        """Delete a contact (admin only)"""
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'success': False, 'message': 'Admin access required'}, 403
            
            contact = Contact.query.get(contact_id)
            
            if not contact:
                return {'success': False, 'message': 'Contact not found'}, 404
            
            db.session.delete(contact)
            db.session.commit()
            
            logger.info(f"Contact {contact_id} deleted by admin {user.username}")
            
            return {
                'success': True,
                'message': 'Contact deleted successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting contact {contact_id}: {str(e)}", exc_info=True)
            return {'success': False, 'message': 'Failed to delete contact'}, 500

class ContactStatsResource(Resource):
    """Get contact statistics (admin only)"""
    
    @jwt_required()
    def get(self):
        try:
            # Verify admin access
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_admin:
                return {'success': False, 'message': 'Admin access required'}, 403
            
            from datetime import datetime, timedelta
            
            total = Contact.query.count()
            unread = Contact.query.filter_by(is_read=False).count()
            
            # Last 7 days
            week_ago = datetime.utcnow() - timedelta(days=7)
            this_week = Contact.query.filter(Contact.created_at >= week_ago).count()
            
            # By service type
            services = db.session.query(
                Contact.service, 
                db.func.count(Contact.id)
            ).group_by(Contact.service).all()
            
            return {
                'success': True,
                'stats': {
                    'total': total,
                    'unread': unread,
                    'this_week': this_week,
                    'by_service': {s[0] or 'General': s[1] for s in services}
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Error getting contact stats: {str(e)}", exc_info=True)
            return {'success': False, 'message': 'Failed to retrieve stats'}, 500