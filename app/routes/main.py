from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models.contact import Contact  # This should be Contact, not ContactMessage
from app.models.project import Project
from app.forms.contact import ContactForm
from app.services.email_service import send_email

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    featured_projects = Project.get_featured()
    return render_template('main/index.html', featured_projects=featured_projects)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@main_bp.route('/projects')
def projects():
    """Projects page"""
    projects = Project.get_all_active()
    return render_template('main/projects.html', projects=projects)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    form = ContactForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Save to database with IP and user agent
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            service=form.service.data,
            message=form.message.data,
            ip_address=request.remote_addr,
            user_agent=str(request.user_agent) if request.user_agent else None
        )
        contact.save()
        
        # Send email notification
        try:
            send_email(
                subject=f"New Contact from {form.name.data}",
                recipients=[current_app.config['ADMIN_EMAIL']],
                body=f"""
Name: {form.name.data}
Email: {form.email.data}
Service: {form.service.data}
Message: {form.message.data}
IP: {request.remote_addr}
                """
            )
            flash('Thank you for your message! I will get back to you within 24 hours.', 'success')
        except Exception as e:
            current_app.logger.error(f"Email failed: {str(e)}")
            flash('Your message has been saved. I will contact you soon.', 'success')
        
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html', form=form)