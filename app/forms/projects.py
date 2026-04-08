from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, URL, Optional

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[Length(max=255)])
    technologies = StringField('Technologies (comma-separated)', validators=[Length(max=255)])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    project_url = StringField('Live Demo URL', validators=[Optional(), URL()])
    featured_image = StringField('Featured Image URL', validators=[Optional(), URL()])
    featured = BooleanField('Featured Project')
    status = SelectField('Status', choices=[('completed', 'Completed'), ('in-progress', 'In Progress'), ('planned', 'Planned')])
    display_order = IntegerField('Display Order', default=0)