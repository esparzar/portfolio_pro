# app/api/resources/contact.py
from flask_restful import Resource, reqparse
from app.models.contact import ContactMessage
from app import db

class ContactMessageResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('subject', type=str, required=True, help='Subject is required')
        parser.add_argument('message', type=str, required=True, help='Message is required')
        args = parser.parse_args()
        
        contact_message = ContactMessage(
            name=args['name'],
            email=args['email'],
            subject=args['subject'],
            message=args['message']
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return {'message': 'Contact message sent successfully'}, 201
