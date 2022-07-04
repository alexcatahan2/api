"""adding user_id column to exercise table

Revision ID: 0d0650d2de3c
Revises: ef1c869becaf
Create Date: 2022-07-04 13:28:48.505608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d0650d2de3c'
down_revision = 'ef1c869becaf'
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
