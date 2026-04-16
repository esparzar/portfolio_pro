import pytest
from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.contact import Contact
from datetime import datetime

@pytest.fixture
def app():
    """Create app for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client, app):
    """Get authentication headers for API tests"""
    with app.app_context():
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    # Login and get token
    response = client.post('/auth/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        token = response.json.get('access_token')
        return {'Authorization': f'Bearer {token}'}
    return {}

# ============================================
# AUTHENTICATION TESTS
# ============================================

def test_login_page(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data or b'Username' in response.data

def test_user_login_success(client, app):
    """Test successful user login"""
    with app.app_context():
        user = User(username='logintest', email='login@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/auth/login', data={
        'username': 'logintest',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_user_login_fail(client, app):
    """Test failed user login"""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_logout(client, app):
    """Test logout functionality"""
    # First login
    with app.app_context():
        user = User(username='logouttest', email='logout@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    client.post('/auth/login', data={
        'username': 'logouttest',
        'password': 'password123'
    })
    
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200

# ============================================
# MAIN ROUTE TESTS
# ============================================

def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_about_page(client):
    """Test about page loads"""
    response = client.get('/about')
    assert response.status_code == 200

def test_projects_page(client):
    """Test projects page loads"""
    response = client.get('/projects')
    assert response.status_code == 200

def test_contact_page(client):
    """Test contact page loads"""
    response = client.get('/contact')
    assert response.status_code == 200

def test_error_404_page(client):
    """Test 404 error page"""
    response = client.get('/nonexistent-page-12345')
    assert response.status_code == 404

# ============================================
# CONTACT FORM TESTS
# ============================================

def test_contact_form_submission(client, app):
    """Test contact form submission"""
    response = client.post('/contact', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'service': 'General Inquiry',
        'message': 'This is a test message for contact form'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with app.app_context():
        contact = Contact.query.filter_by(email='john@example.com').first()
        assert contact is not None
        assert contact.name == 'John Doe'
        assert contact.message == 'This is a test message for contact form'

def test_contact_form_invalid_email(client):
    """Test contact form with invalid email"""
    response = client.post('/contact', data={
        'name': 'John Doe',
        'email': 'invalid-email',
        'service': 'General Inquiry',
        'message': 'Test message'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_contact_form_empty_fields(client):
    """Test contact form with empty fields"""
    response = client.post('/contact', data={
        'name': '',
        'email': '',
        'message': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200

# ============================================
# PROJECT MODEL TESTS
# ============================================

def test_project_creation(app):
    """Test project model creation"""
    with app.app_context():
        project = Project(
            title='Test Project',
            description='This is a test description for the project',
            short_description='Short description',
            technologies='Python, Flask, PostgreSQL',
            featured=True,
            status='completed',
            display_order=1
        )
        db.session.add(project)
        db.session.commit()
        
        assert project.id is not None
        assert project.title == 'Test Project'
        assert project.featured == True

def test_project_to_dict(app):
    """Test project to_dict method"""
    with app.app_context():
        project = Project(
            title='Test Project',
            description='Test description',
            technologies='Python, Flask',
            featured=True,
            status='completed'
        )
        db.session.add(project)
        db.session.commit()
        
        project_dict = project.to_dict()
        
        assert project_dict['title'] == 'Test Project'
        assert 'Python' in project_dict.get('technologies', '')
        assert project_dict.get('featured') == True
        assert project_dict.get('status') == 'completed'

def test_project_technologies_list(app):
    """Test project technologies parsing"""
    with app.app_context():
        project = Project(
            title='Test Project',
            description='Test',
            technologies='Python, Flask, SQLAlchemy, PostgreSQL'
        )
        
        techs = project.get_technologies_list()
        assert len(techs) == 4
        assert 'Python' in techs
        assert 'Flask' in techs

def test_get_featured_projects(app):
    """Test get_featured projects method"""
    with app.app_context():
        project1 = Project(title='Featured 1', description='Test', featured=True)
        project2 = Project(title='Featured 2', description='Test', featured=True)
        project3 = Project(title='Not Featured', description='Test', featured=False)
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        
        featured = Project.get_featured()
        assert len(featured) == 2

def test_get_all_active_projects(app):
    """Test get_all_active projects method"""
    with app.app_context():
        project1 = Project(title='Active 1', description='Test', is_active=True)
        project2 = Project(title='Active 2', description='Test', is_active=True)
        project3 = Project(title='Inactive', description='Test', is_active=False)
        db.session.add_all([project1, project2, project3])
        db.session.commit()
        
        active = Project.get_all_active()
        assert len(active) == 2

# ============================================
# API TESTS
# ============================================

def test_api_contact_submission(client, app):
    """Test API contact submission"""
    response = client.post('/api/contacts', json={
        'name': 'API Test User',
        'email': 'api@example.com',
        'service': 'API Test Service',
        'message': 'Testing API contact submission'
    })
    
    assert response.status_code == 201
    
    with app.app_context():
        contact = Contact.query.filter_by(email='api@example.com').first()
        assert contact is not None
        assert contact.name == 'API Test User'

def test_api_contact_invalid_email(client):
    """Test API contact with invalid email"""
    response = client.post('/api/contacts', json={
        'name': 'API Test',
        'email': 'invalid',
        'message': 'Test'
    })
    
    assert response.status_code == 400

def test_api_get_projects(client, app):
    """Test API get projects"""
    with app.app_context():
        project = Project(
            title='API Test Project',
            description='Test description for API',
            featured=True,
            is_active=True
        )
        db.session.add(project)
        db.session.commit()
    
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert 'projects' in data or isinstance(data, list)

def test_api_get_single_project(client, app):
    """Test API get single project"""
    with app.app_context():
        project = Project(
            title='Single Project Test',
            description='Test',
            is_active=True
        )
        db.session.add(project)
        db.session.commit()
        project_id = project.id
    
    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 200

def test_api_get_nonexistent_project(client):
    """Test API get nonexistent project"""
    response = client.get('/api/projects/99999')
    assert response.status_code == 404

# ============================================
# USER MODEL TESTS
# ============================================

def test_user_creation(app):
    """Test user model creation"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            is_admin=False,
            is_active=True
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.check_password('password123')

def test_user_password_hashing(app):
    """Test user password hashing"""
    with app.app_context():
        user = User(username='hashuser', email='hash@example.com')
        user.set_password('mypassword')
        
        assert user.password_hash != 'mypassword'
        assert user.check_password('mypassword') == True
        assert user.check_password('wrong') == False

def test_user_authentication(app):
    """Test user authentication method"""
    with app.app_context():
        user = User(username='authuser', email='auth@example.com')
        user.set_password('secret123')
        db.session.add(user)
        db.session.commit()
        
        authenticated = User.authenticate('authuser', 'secret123')
        assert authenticated is not None
        assert authenticated.username == 'authuser'
        
        not_authenticated = User.authenticate('authuser', 'wrong')
        assert not_authenticated is None

def test_user_to_dict(app):
    """Test user to_dict method"""
    with app.app_context():
        user = User(
            username='dictuser',
            email='dict@example.com',
            is_admin=True,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        
        assert user_dict['username'] == 'dictuser'
        assert user_dict['email'] == 'dict@example.com'
        assert user_dict['is_admin'] == True
        assert 'password_hash' not in user_dict  # Security: don't expose password

# ============================================
# CONTACT MODEL TESTS
# ============================================

def test_contact_creation(app):
    """Test contact model creation"""
    with app.app_context():
        contact = Contact(
            name='Contact User',
            email='contact@example.com',
            service='Support',
            message='This is a support message',
            ip_address='127.0.0.1',
            user_agent='Test Agent'
        )
        db.session.add(contact)
        db.session.commit()
        
        assert contact.id is not None
        assert contact.name == 'Contact User'
        assert contact.is_read == False

def test_contact_to_dict(app):
    """Test contact to_dict method"""
    with app.app_context():
        contact = Contact(
            name='Dict Contact',
            email='dictcontact@example.com',
            service='Sales',
            message='Sales inquiry message'
        )
        db.session.add(contact)
        db.session.commit()
        
        contact_dict = contact.to_dict()
        
        assert contact_dict['name'] == 'Dict Contact'
        assert contact_dict['email'] == 'dictcontact@example.com'
        assert contact_dict['service'] == 'Sales'
        assert 'created_at' in contact_dict

def test_contact_mark_as_read(app):
    """Test contact mark as read method"""
    with app.app_context():
        contact = Contact(
            name='Read Test',
            email='read@example.com',
            message='Test message'
        )
        db.session.add(contact)
        db.session.commit()
        
        assert contact.is_read == False
        
        Contact.mark_as_read(contact.id)
        db.session.refresh(contact)
        assert contact.is_read == True

def test_contact_get_unread(app):
    """Test get unread contacts method"""
    with app.app_context():
        contact1 = Contact(name='Unread 1', email='unread1@example.com', message='Test', is_read=False)
        contact2 = Contact(name='Unread 2', email='unread2@example.com', message='Test', is_read=False)
        contact3 = Contact(name='Read', email='read@example.com', message='Test', is_read=True)
        db.session.add_all([contact1, contact2, contact3])
        db.session.commit()
        
        unread = Contact.get_unread()
        assert len(unread) == 2

# ============================================
# ADMIN TESTS
# ============================================

def test_admin_dashboard_redirects_to_login(client):
    """Test admin dashboard requires authentication"""
    response = client.get('/admin/')
    assert response.status_code == 302  # Redirect to login

def test_admin_projects_redirects_to_login(client):
    """Test admin projects requires authentication"""
    response = client.get('/admin/projects')
    assert response.status_code == 302

def test_admin_contacts_redirects_to_login(client):
    """Test admin contacts requires authentication"""
    response = client.get('/admin/contacts')
    assert response.status_code == 302

# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    pytest.main(['-v', '--tb=short', __file__])