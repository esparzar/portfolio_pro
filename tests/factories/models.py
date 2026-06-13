import factory

from app import db
from app.models.contact import Contact
from app.models.project import Project
from app.models.user import User


class SQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_admin = False
    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password(extracted or "password123")


class ProjectFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project {n}")
    description = "A useful portfolio project."
    short_description = "Short project summary"
    technologies = "Python, Flask, PostgreSQL"
    status = "completed"
    featured = False
    display_order = 0


class ContactFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Contact

    name = "Contact User"
    email = factory.Sequence(lambda n: f"contact{n}@example.com")
    service = "other"
    message = "This is a detailed contact message."
    is_read = False
