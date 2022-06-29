"""add content column to post table

Revision ID: 601018dd98b7
Revises: 8c2dd91d356f
Create Date: 2022-06-29 15:34:29.487106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '601018dd98b7'
down_revision = '8c2dd91d356f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
