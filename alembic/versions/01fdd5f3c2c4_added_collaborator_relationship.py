"""added collaborator relationship

Revision ID: 01fdd5f3c2c4
Revises: c15fcbccb3e3
Create Date: 2021-10-17 22:24:12.672047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01fdd5f3c2c4'
down_revision = 'c15fcbccb3e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collaborator',
    sa.Column('user_id', sa.String(length=256), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id')
    )
    op.alter_column('course', 'title',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.alter_column('course', 'length',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.alter_column('course', 'teacher',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.alter_column('course', 'subject',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=256),
               existing_nullable=False)
    op.create_index(op.f('ix_course_id'), 'course', ['id'], unique=False)
    op.create_index(op.f('ix_course_subject'), 'course', ['subject'], unique=False)
    op.drop_column('student', 'id')
    op.alter_column('user_account', 'user_id',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               nullable=True)
    op.alter_column('user_account', 'first_name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=True)
    op.alter_column('user_account', 'last_name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=True)
    op.alter_column('user_account', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_index('user_account_email_idx', table_name='user_account')
    op.drop_index('user_account_user_id_idx', table_name='user_account')
    op.drop_constraint('user_account_user_id_key', 'user_account', type_='unique')
    op.create_index(op.f('ix_user_account_email'), 'user_account', ['email'], unique=False)
    op.create_index(op.f('ix_user_account_id'), 'user_account', ['id'], unique=False)
    op.create_index(op.f('ix_user_account_user_id'), 'user_account', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_account_user_id'), table_name='user_account')
    op.drop_index(op.f('ix_user_account_id'), table_name='user_account')
    op.drop_index(op.f('ix_user_account_email'), table_name='user_account')
    op.create_unique_constraint('user_account_user_id_key', 'user_account', ['user_id'])
    op.create_index('user_account_user_id_idx', 'user_account', ['user_id'], unique=False)
    op.create_index('user_account_email_idx', 'user_account', ['email'], unique=False)
    op.alter_column('user_account', 'is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('user_account', 'last_name',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('user_account', 'first_name',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.alter_column('user_account', 'user_id',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               nullable=False)
    op.add_column('student', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_course_subject'), table_name='course')
    op.drop_index(op.f('ix_course_id'), table_name='course')
    op.alter_column('course', 'subject',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    op.alter_column('course', 'teacher',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)
    op.alter_column('course', 'length',
               existing_type=sa.String(length=256),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('course', 'title',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_table('collaborator')
    # ### end Alembic commands ###
