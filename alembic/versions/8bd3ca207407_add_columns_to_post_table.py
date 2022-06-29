"""add columns to post table

Revision ID: 8bd3ca207407
Revises: b26cbb419d18
Create Date: 2022-06-29 15:51:31.702576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bd3ca207407'
down_revision = 'b26cbb419d18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                    server_default = sa.text('now()')))     
    pass            


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
