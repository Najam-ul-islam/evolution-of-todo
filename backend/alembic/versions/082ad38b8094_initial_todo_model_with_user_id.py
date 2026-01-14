"""Initial Todo model with user_id

Revision ID: 082ad38b8094
Revises:
Create Date: 2026-01-11 09:36:51.552107

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '082ad38b8094'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the todos table with user_id foreign key
    op.create_table(
        'todo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    # Drop the todos table
    op.drop_table('todo')