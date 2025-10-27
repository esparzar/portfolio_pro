# app/routes/main.py
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/projects')
def projects():
    return render_template('main/projects.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Portfolio API is running'})
