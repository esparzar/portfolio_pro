from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.admin.decorators import admin_required
from app.forms.projects import ProjectForm
from app.models.contact import Contact
from app.models.project import Project
from app.models.user import User

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    projects_count = Project.query.count()
    contacts_count = Contact.query.count()
    users_count = User.query.count()
    unread_messages = Contact.query.filter_by(is_read=False).count()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        projects_count=projects_count,
        contacts_count=contacts_count,
        users_count=users_count,
        unread_messages=unread_messages,
        recent_contacts=recent_contacts,
    )


@admin_bp.route("/projects")
@login_required
@admin_required
def projects():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = Project.query.order_by(Project.display_order).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )
    return render_template("admin/projects.html", projects=pagination.items, pagination=pagination)


@admin_bp.route("/projects/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_project():
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
            images=form.images.data,
            featured=form.featured.data,
            status=form.status.data,
            display_order=form.display_order.data,
        )
        db.session.add(project)
        db.session.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for("admin.projects"))

    return render_template("admin/project_form.html", form=form, title="Add Project")


@admin_bp.route("/projects/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_project(id):
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
        project.images = form.images.data
        project.featured = form.featured.data
        project.status = form.status.data
        project.display_order = form.display_order.data
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for("admin.projects"))

    return render_template(
        "admin/project_form.html", form=form, title="Edit Project", project=project
    )


@admin_bp.route("/projects/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("admin.projects"))


@admin_bp.route("/contacts")
@login_required
@admin_required
def contacts():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = Contact.query.order_by(Contact.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )
    return render_template("admin/contacts.html", contacts=pagination.items, pagination=pagination)


@admin_bp.route("/contacts/view/<int:id>")
@login_required
@admin_required
def view_contact(id):
    contact = Contact.query.get_or_404(id)
    if not contact.is_read:
        contact.is_read = True
        db.session.commit()

    return render_template("admin/contact_detail.html", contact=contact)


@admin_bp.route("/contacts/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect(url_for("admin.contacts"))
