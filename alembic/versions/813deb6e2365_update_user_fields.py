"""update user fields

Revision ID: 813deb6e2365
Revises: ef98f1dea6cb
Create Date: 2022-07-03 14:37:51.837045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '813deb6e2365'
down_revision = 'ef98f1dea6cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('firstName', sa.String, nullable = sa.false, server_default = 'john'))
    op.add_column('users', sa.Column('lastName', sa.String, nullable = sa.false, server_default = 'doe'))
    pass


def downgrade() -> None:
    op.drop_column('users', 'firstName')
    op.drop_column('users', 'lastName')
    pass
