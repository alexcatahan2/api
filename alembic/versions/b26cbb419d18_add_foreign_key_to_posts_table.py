"""add foreign key to posts table

Revision ID: b26cbb419d18
Revises: 2cac793b3560
Create Date: 2022-06-29 15:45:41.783418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b26cbb419d18'
down_revision = '2cac793b3560'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table='users',
                         local_cols=["owner_id"], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
