"""Add MTO export tracking

Revision ID: 006
Revises: 005
Create Date: 2024-03-20 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create mto_exports table
    op.create_table(
        'mto_exports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('export_type', sa.String(length=50), nullable=False),
        sa.Column('export_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('record_count', sa.Integer(), nullable=False),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create mto_export_records table
    op.create_table(
        'mto_export_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('export_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('record_type', sa.String(length=50), nullable=False),
        sa.Column('record_data', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['export_id'], ['mto_exports.id'], ),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create mto_export_logs table
    op.create_table(
        'mto_export_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('export_id', sa.Integer(), nullable=False),
        sa.Column('log_level', sa.String(length=20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['export_id'], ['mto_exports.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('mto_export_logs')
    op.drop_table('mto_export_records')
    op.drop_table('mto_exports') 