"""add title and description to lesson entity and username to user entity

Revision ID: 43da115dd3f4
Revises: ffea6616a1aa
Create Date: 2021-11-08 22:05:37.764777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43da115dd3f4'
down_revision = 'ffea6616a1aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lesson', sa.Column('title', sa.String(length=150), nullable=True))
    op.add_column('lesson', sa.Column('description', sa.String(length=256), nullable=True))
    op.add_column('user_account', sa.Column('username', sa.String(length=30), nullable=True))
    # Added to be consistent with existing data on table
    op.execute("UPDATE lesson SET title = 'Backward compatibility title'")
    op.alter_column('lesson', 'title', nullable=False)
    op.execute("UPDATE user_account SET username = 'Bruce_wayne'")
    op.alter_column('user_account', 'username', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'username')
    op.drop_column('lesson', 'description')
    op.drop_column('lesson', 'title')
    # ### end Alembic commands ###
