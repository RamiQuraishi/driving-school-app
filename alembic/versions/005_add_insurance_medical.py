"""Add insurance and medical tracking

Revision ID: 005
Revises: 004
Create Date: 2024-03-20 10:04:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create insurance_policies table
    op.create_table(
        'insurance_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('policy_number', sa.String(length=50), nullable=False),
        sa.Column('provider', sa.String(length=100), nullable=False),
        sa.Column('coverage_type', sa.String(length=50), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('coverage_amount', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('policy_number')
    )

    # Create vehicle_insurance table
    op.create_table(
        'vehicle_insurance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['policy_id'], ['insurance_policies.id'], ),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create medical_certificates table
    op.create_table(
        'medical_certificates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('certificate_number', sa.String(length=50), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('issuing_authority', sa.String(length=100), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('certificate_number')
    )

    # Create medical_conditions table
    op.create_table(
        'medical_conditions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('condition_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('medical_conditions')
    op.drop_table('medical_certificates')
    op.drop_table('vehicle_insurance')
    op.drop_table('insurance_policies') 