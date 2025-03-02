"""Initial migration

Revision ID: 05daa24550bd
Revises: None
Create Date: 2025-03-02 10:33:42.381

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05daa24550bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the initial tables
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, index=True),
        sa.Column('description', sa.String, index=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
    )


def downgrade():
    # Drop the initial tables
    op.drop_table('items')
    op.drop_table('users')
