"""changing length data type to Time in workout table

Revision ID: 4399d16edea2
Revises: f03b4261ab21
Create Date: 2022-07-06 21:30:22.757747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4399d16edea2'
down_revision = 'f03b4261ab21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('workouts', 'length')
    op.add_column('workouts', sa.Column('length', sa.Time(), nullable = False, server_default = sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('workouts', 'length')
    op.add_column('workouts', sa.Column('length', sa.Integer(), nullable = False, server_default= '0'))
    pass
