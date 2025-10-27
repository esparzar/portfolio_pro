# app/models/contact.py
from app import db
from datetime import datetime
import enum

class MessageStatus(enum.Enum):
    NEW = 'new'
    READ = 'read'
    REPLIED = 'replied'
    ARCHIVED = 'archived'

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))  # Store IPv6 addresses if needed
    user_agent = db.Column(db.Text)
    status = db.Column(db.Enum(MessageStatus), default=MessageStatus.NEW)
    replied_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'ip_address': self.ip_address,
            'status': self.status.value,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def mark_as_read(self):
        self.status = MessageStatus.READ
        db.session.commit()

    def mark_as_replied(self):
        self.status = MessageStatus.REPLIED
        self.replied_at = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<ContactMessage from {self.name} - {self.subject}>'
