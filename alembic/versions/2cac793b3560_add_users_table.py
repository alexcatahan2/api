"""add users table

Revision ID: 2cac793b3560
Revises: 601018dd98b7
Create Date: 2022-06-29 15:38:50.300250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cac793b3560'
down_revision = '601018dd98b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')  
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

