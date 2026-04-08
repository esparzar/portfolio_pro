from datetime import datetime
from app import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def save(self):
        """Save contact to database"""
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_unread(cls):
        """Get all unread messages"""
        return cls.query.filter_by(is_read=False).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_all(cls):
        """Get all messages"""
        return cls.query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def mark_as_read(cls, contact_id):
        """Mark message as read"""
        contact = cls.query.get(contact_id)
        if contact:
            contact.is_read = True
            db.session.commit()
            return True
        return False
    
    def to_dict(self):
        """Convert contact to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'service': self.service,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }