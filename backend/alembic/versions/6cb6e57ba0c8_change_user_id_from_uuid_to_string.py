"""Change user_id from UUID to String

Revision ID: 6cb6e57ba0c8
Revises: 082ad38b8094
Create Date: 2026-01-19 20:41:57.053458

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6cb6e57ba0c8'
down_revision = '082ad38b8094'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop foreign key constraints before changing column types
    op.drop_constraint('todo_user_id_fkey', 'todo', type_='foreignkey')
    op.drop_constraint('todos_user_id_fkey', 'todos', type_='foreignkey')

    # Change user_id column from UUID to String in todo table
    op.alter_column('todo', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.String(length=255),
               nullable=True)

    # Change user_id column from UUID to String in todos table
    op.alter_column('todos', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.String(length=255),
               nullable=True)

    # Change user_id column from UUID to String in conversations table
    op.alter_column('conversations', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.String(length=255),
               existing_nullable=False)


def downgrade() -> None:
    # Change user_id column back from String to UUID in conversations table
    op.alter_column('conversations', 'user_id',
               existing_type=sa.String(length=255),
               type_=sa.UUID(),
               existing_nullable=False)

    # Change user_id column back from String to UUID in todos table
    op.alter_column('todos', 'user_id',
               existing_type=sa.String(length=255),
               type_=sa.UUID(),
               nullable=False)

    # Change user_id column back from String to UUID in todo table
    op.alter_column('todo', 'user_id',
               existing_type=sa.String(length=255),
               type_=sa.UUID(),
               nullable=False)

    # Recreate foreign key constraints (assuming the referenced tables exist)
    # We'll skip recreating them to avoid complications if the referenced tables don't exist