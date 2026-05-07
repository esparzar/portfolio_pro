"""Add project and contact indexes.

Revision ID: c2f9f5f7a1b4
Revises: 9eaa46020718
Create Date: 2026-05-07 16:00:00.000000
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "c2f9f5f7a1b4"
down_revision = "9eaa46020718"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_contacts_created_at", "contacts", ["created_at"], unique=False)
    op.create_index("ix_contacts_email", "contacts", ["email"], unique=False)
    op.create_index("ix_contacts_is_read", "contacts", ["is_read"], unique=False)
    op.create_index("ix_contacts_service", "contacts", ["service"], unique=False)
    op.create_index("ix_projects_created_at", "projects", ["created_at"], unique=False)
    op.create_index("ix_projects_display_order", "projects", ["display_order"], unique=False)
    op.create_index("ix_projects_featured", "projects", ["featured"], unique=False)
    op.create_index("ix_projects_status", "projects", ["status"], unique=False)
    op.create_index("ix_projects_title", "projects", ["title"], unique=False)


def downgrade():
    op.drop_index("ix_projects_title", table_name="projects")
    op.drop_index("ix_projects_status", table_name="projects")
    op.drop_index("ix_projects_featured", table_name="projects")
    op.drop_index("ix_projects_display_order", table_name="projects")
    op.drop_index("ix_projects_created_at", table_name="projects")
    op.drop_index("ix_contacts_service", table_name="contacts")
    op.drop_index("ix_contacts_is_read", table_name="contacts")
    op.drop_index("ix_contacts_email", table_name="contacts")
    op.drop_index("ix_contacts_created_at", table_name="contacts")
