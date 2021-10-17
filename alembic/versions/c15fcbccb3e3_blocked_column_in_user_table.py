"""blocked column in user table

Revision ID: c15fcbccb3e3
Revises: 6816ba8dcc84
Create Date: 2021-10-17 10:31:17.848034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c15fcbccb3e3'
down_revision = '6816ba8dcc84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('blocked', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'blocked')
    # ### end Alembic commands ###
