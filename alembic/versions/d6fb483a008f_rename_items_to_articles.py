"""Rename items to articles

Revision ID: d6fb483a008f
Revises: f5736ede362c
Create Date: 2025-03-02 10:33:42.381

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd6fb483a008f'
down_revision = 'f5736ede362c'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('items', 'articles')


def downgrade():
    op.rename_table('articles', 'items')
