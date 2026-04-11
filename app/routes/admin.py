from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.contact import Contact
from app.models.user import User
from app.forms.projects import ProjectForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))
    
    projects_count = Project.query.count()
    contacts_count = Contact.query.count()
    users_count = User.query.count()
    unread_messages = Contact.query.filter_by(is_read=False).count()
    
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         projects_count=projects_count,
                         contacts_count=contacts_count,
                         users_count=users_count,
                         unread_messages=unread_messages,
                         recent_contacts=recent_contacts)

@admin_bp.route('/projects')
@login_required
def projects():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    projects = Project.query.order_by(Project.display_order).all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            short_description=form.short_description.data,
            technologies=form.technologies.data,
            github_url=form.github_url.data,
            project_url=form.project_url.data,
            featured_image=form.featured_image.data,
            featured=form.featured.data,
            status=form.status.data,
            display_order=form.display_order.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', form=form, title='Add Project')

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.short_description = form.short_description.data
        project.technologies = form.technologies.data
        project.github_url = form.github_url.data
        project.project_url = form.project_url.data
        project.featured_image = form.featured_image.data
        project.featured = form.featured.data
        project.status = form.status.data
        project.display_order = form.display_order.data
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', form=form, title='Edit Project', project=project)

@admin_bp.route('/projects/delete/<int:id>')
@login_required
def delete_project(id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

@admin_bp.route('/contacts')
@login_required
def contacts():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@admin_bp.route('/contacts/view/<int:id>')
@login_required
def view_contact(id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    contact = Contact.query.get_or_404(id)
    if not contact.is_read:
        contact.is_read = True
        db.session.commit()
    
    return render_template('admin/contact_detail.html', contact=contact)

@admin_bp.route('/contacts/delete/<int:id>')
@login_required
def delete_contact(id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.contacts'))

@admin_bp.route('/setup-admin')
def setup_admin():
    """Create admin user using password from environment variables"""
    from app import db
    from app.models.user import User
    import os
    
    try:
        # Get admin credentials from environment variables
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD')
        
        # Check if admin already exists
        admin_exists = User.query.filter_by(username=username).first()
        
        if admin_exists:
            return f'''
            <h2>Admin User Already Exists</h2>
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Email:</strong> {email}</p>
            <br>
            <a href="/auth/login">Click here to login →</a>
            '''
        
        # Check if password is set in environment
        if not password:
            return '''
            <h2>⚠️ Error: ADMIN_PASSWORD not set in environment variables</h2>
            <p>Please add ADMIN_PASSWORD to your Render environment variables.</p>
            <p>Then redeploy and visit this page again.</p>
            '''
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            is_admin=True,
            is_active=True
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        
        return f'''
        <h2>✅ Admin User Created Successfully!</h2>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Password:</strong> (the password you set in ADMIN_PASSWORD)</p>
        <br>
        <a href="/auth/login">Click here to login →</a>
        <br><br>
        <p><strong>IMPORTANT:</strong> After logging in, remove this page for security!</p>
        '''
    
    except Exception as e:
        return f'<h2>Error:</h2><p>{str(e)}</p>'
   