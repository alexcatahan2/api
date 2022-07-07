"""adding users_id to exercise table

Revision ID: f03b4261ab21
Revises: 6be693d1d22a
Create Date: 2022-07-06 20:46:01.703090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03b4261ab21'
down_revision = '6be693d1d22a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('exercises', sa.Column('user_id', sa.Integer(), nullable = False))
    op.create_foreign_key('exercises_users_fk', source_table='exercises', referent_table='users',
                            local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('exercises_users_fk', table_name='exercises')
    op.drop_column('exercises', 'user_id')
    pass
