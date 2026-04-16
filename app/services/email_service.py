import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def send_email(subject, recipients, body, html=None):
    """Send email using SMTP"""
    if isinstance(recipients, str):
        recipients = [recipients]
    
    if current_app.config.get('DEBUG'):
        logging.info(f"Email would be sent: {subject} to {recipients}")
        return True
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = ', '.join(recipients)
        
        msg.attach(MIMEText(body, 'plain'))
        if html:
            msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            server.send_message(msg)
        
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False

def send_contact_notification(contact):
    """Send notification for new contact submission"""
    subject = f"New Contact: {contact.name}"
    body = f"""
New contact submission:

Name: {contact.name}
Email: {contact.email}
Service: {contact.service}
Message: {contact.message}
    """
    
    admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@example.com')
    return send_email(subject, admin_email, body)
