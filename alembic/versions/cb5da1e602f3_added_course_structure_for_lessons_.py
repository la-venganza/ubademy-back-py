"""added course structure for lessons, exams and questions

Revision ID: cb5da1e602f3
Revises: 15d39f9984b6
Create Date: 2021-10-26 21:11:56.049240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb5da1e602f3'
down_revision = '15d39f9984b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exam',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('minimum_qualification', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exam_id'), 'exam', ['id'], unique=False)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('sequence_number', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_id'), 'question', ['id'], unique=False)
    op.create_table('develop_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_develop_question_id'), 'develop_question', ['id'], unique=False)
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('require', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('sequence_number', sa.Integer(), nullable=False),
    sa.Column('multimedia_id', sa.String(length=256), nullable=False),
    sa.Column('multimedia_type', sa.String(length=30), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_id'), 'lesson', ['id'], unique=False)
    op.create_table('multiple_choice_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=256), nullable=False),
    sa.Column('amount_of_options', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_multiple_choice_question_id'), 'multiple_choice_question', ['id'], unique=False)
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('multiple_choice_question_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=256), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['multiple_choice_question_id'], ['multiple_choice_question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_choice_id'), 'choice', ['id'], unique=False)
    op.add_column('course', sa.Column('description', sa.String(length=256), nullable=True))
    op.add_column('course', sa.Column('type', sa.String(length=50), nullable=True))
    op.add_column('course', sa.Column('location', sa.String(length=100), nullable=True))
    op.add_column('course', sa.Column('hashtags', sa.String(length=256), nullable=True))
    op.add_column('course', sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_index('ix_course_subject', table_name='course')
    op.create_index(op.f('ix_course_hashtags'), 'course', ['hashtags'], unique=False)
    op.drop_column('course', 'year')
    op.drop_column('course', 'length')
    op.drop_column('course', 'teacher')
    op.drop_column('course', 'subject')
    # Added to be consistent with existing data on table
    op.execute("UPDATE course SET type = 'IA'")
    op.alter_column('course', 'type', nullable=False)
    op.execute("UPDATE course SET hashtags = 'IA'")
    op.alter_column('course', 'hashtags', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('subject', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('teacher', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('length', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.add_column('course', sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_course_hashtags'), table_name='course')
    op.create_index('ix_course_subject', 'course', ['subject'], unique=False)
    op.drop_column('course', 'creation_date')
    op.drop_column('course', 'hashtags')
    op.drop_column('course', 'location')
    op.drop_column('course', 'type')
    op.drop_column('course', 'description')
    # Added to be consistent with existing data on table ##
    op.execute("UPDATE course SET subject = 'IA'")
    op.alter_column('course', 'subject', nullable=False)
    op.execute("UPDATE course SET teacher = 'ANY'")
    op.alter_column('course', 'teacher', nullable=False)
    op.execute("UPDATE course SET length = 0")
    op.alter_column('course', 'length', nullable=False)
    op.execute("UPDATE course SET year = 2000")
    op.alter_column('course', 'year', nullable=False)
    #                                                   ##
    op.drop_index(op.f('ix_choice_id'), table_name='choice')
    op.drop_table('choice')
    op.drop_index(op.f('ix_multiple_choice_question_id'), table_name='multiple_choice_question')
    op.drop_table('multiple_choice_question')
    op.drop_index(op.f('ix_lesson_id'), table_name='lesson')
    op.drop_table('lesson')
    op.drop_index(op.f('ix_develop_question_id'), table_name='develop_question')
    op.drop_table('develop_question')
    op.drop_index(op.f('ix_question_id'), table_name='question')
    op.drop_table('question')
    op.drop_index(op.f('ix_exam_id'), table_name='exam')
    op.drop_table('exam')
    # ### end Alembic commands ###
