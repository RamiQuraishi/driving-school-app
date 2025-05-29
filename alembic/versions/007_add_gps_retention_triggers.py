"""Add GPS retention triggers

Revision ID: 007
Revises: 006
Create Date: 2024-03-20 10:06:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create gps_tracking table
    op.create_table(
        'gps_tracking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('speed', sa.Float(), nullable=True),
        sa.Column('heading', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create gps_retention_policies table
    op.create_table(
        'gps_retention_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('retention_days', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create gps_retention_logs table
    op.create_table(
        'gps_retention_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.Integer(), nullable=False),
        sa.Column('records_deleted', sa.Integer(), nullable=False),
        sa.Column('execution_time', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['policy_id'], ['gps_retention_policies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create trigger for automatic GPS data cleanup
    op.execute("""
        CREATE TRIGGER IF NOT EXISTS cleanup_old_gps_data
        AFTER INSERT ON gps_tracking
        BEGIN
            DELETE FROM gps_tracking
            WHERE timestamp < datetime('now', '-30 days');
        END;
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS cleanup_old_gps_data;")
    
    # Drop tables
    op.drop_table('gps_retention_logs')
    op.drop_table('gps_retention_policies')
    op.drop_table('gps_tracking') 