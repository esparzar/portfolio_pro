from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    service = SelectField('Service', choices=[
        ('', 'Select a service'),
        ('api', 'REST API Development'),
        ('flask', 'Flask Application'),
        ('docker', 'Docker Deployment'),
        ('database', 'Database Design'),
        ('other', 'Other')
    ])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])