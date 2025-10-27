# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Temporary implementation - we'll add forms later
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Temporary implementation - we'll add forms later
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
