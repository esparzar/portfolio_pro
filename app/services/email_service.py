import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging

def send_email(subject, recipients, body, html=None):
    """
    Send email using SMTP
    
    Args:
        subject: Email subject
        recipients: List of email addresses or single string
        body: Plain text email body
        html: HTML email body (optional)
    """
    if isinstance(recipients, str):
        recipients = [recipients]
    
    # For development, just log the email
    if current_app.config.get('DEBUG'):
        logging.info(f"Email would be sent: {subject} to {recipients}")
        logging.info(f"Body: {body}")
        return True
    
    # Production email sending
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = current_app.config['SMTP_USERNAME']
        msg['To'] = ', '.join(recipients)
        
        # Attach plain text part
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach HTML part if provided
        if html:
            msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.send_message(msg)
        
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False