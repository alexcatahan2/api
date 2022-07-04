"""adding workout table 

Revision ID: 6be693d1d22a
Revises: 813deb6e2365
Create Date: 2022-07-03 19:45:28.533743

"""
from time import time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6be693d1d22a'
down_revision = '813deb6e2365'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("workouts", 
                    sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                    sa.Column('start', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')),
                    sa.Column('stop', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')), 
                    sa.Column('length', sa.Integer(), nullable = False, server_default= '0'),
                    sa.Column('date', sa.Date(), nullable = False, server_default = sa.text('CURRENT_DATE')),
                    sa.Column('user_id', sa.Integer, nullable = False))
    op.create_table('exercises', 
                    sa.Column('exercise_id', sa.Integer(), primary_key = True, nullable = False),
                    sa.Column('workout_id', sa.Integer(), nullable = False), 
                    sa.Column('type', sa.String(), nullable = False, server_default = 'exercise'),
                    sa.Column('repititions', sa.Integer(), nullable = False, server_default = '10'),
                    sa.Column('weight', sa.Integer(), nullable = False),
                    sa.Column('start', sa.TIMESTAMP(timezone=True), nullable = False, server_default= sa.text('now()')),
                    sa.Column('stop', sa.TIMESTAMP(timezone=True), nullable = False, server_default= sa.text('now()')))   
    op.create_foreign_key('workouts_users_fk', source_table='workouts', referent_table='users',
                            local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('exercises_workouts_fk', source_table='exercises', referent_table='workouts',
                            local_cols=['workout_id'], remote_cols=['id'], ondelete="CASCADE")
 
    pass



def downgrade() -> None:
    op.drop_constraint('workouts_users_fk', table_name='workouts')
    op.drop_constraint('exercises_workouts_fk', table_name='exercises')
    op.drop_table('workouts')
    op.drop_table('exercises')
    pass
