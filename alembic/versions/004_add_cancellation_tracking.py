"""Add cancellation tracking

Revision ID: 004
Revises: 003
Create Date: 2024-03-20 10:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create cancellations table
    op.create_table(
        'cancellations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('cancelled_by_id', sa.Integer(), nullable=False),
        sa.Column('cancellation_type', sa.String(length=50), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('cancelled_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['cancelled_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create cancellation_policies table
    op.create_table(
        'cancellation_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('hours_before_lesson', sa.Integer(), nullable=False),
        sa.Column('fee_amount', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create cancellation_fees table
    op.create_table(
        'cancellation_fees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cancellation_id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['cancellation_id'], ['cancellations.id'], ),
        sa.ForeignKeyConstraint(['policy_id'], ['cancellation_policies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('cancellation_fees')
    op.drop_table('cancellation_policies')
    op.drop_table('cancellations') 