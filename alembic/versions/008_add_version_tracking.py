"""Add version tracking

Revision ID: 008
Revises: 007
Create Date: 2024-03-20 10:07:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create version_tracking table
    op.create_table(
        'version_tracking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('table_name', sa.String(length=100), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('changed_by_id', sa.Integer(), nullable=False),
        sa.Column('changed_at', sa.DateTime(), nullable=False),
        sa.Column('change_type', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['changed_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create version_conflicts table
    op.create_table(
        'version_conflicts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('table_name', sa.String(length=100), nullable=False),
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('version1_id', sa.Integer(), nullable=False),
        sa.Column('version2_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('resolved_by_id', sa.Integer(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['resolved_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['version1_id'], ['version_tracking.id'], ),
        sa.ForeignKeyConstraint(['version2_id'], ['version_tracking.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create triggers for version tracking
    op.execute("""
        CREATE TRIGGER IF NOT EXISTS track_student_changes
        AFTER UPDATE ON students
        BEGIN
            INSERT INTO version_tracking (
                table_name, record_id, version, data, changed_by_id,
                changed_at, change_type, created_at
            )
            VALUES (
                'students',
                NEW.id,
                COALESCE((SELECT MAX(version) + 1 FROM version_tracking 
                         WHERE table_name = 'students' AND record_id = NEW.id), 1),
                json_object(
                    'id', NEW.id,
                    'user_id', NEW.user_id,
                    'license_number', NEW.license_number,
                    'license_class', NEW.license_class,
                    'license_expiry', NEW.license_expiry,
                    'address', NEW.address,
                    'phone', NEW.phone,
                    'emergency_contact', NEW.emergency_contact
                ),
                (SELECT id FROM users WHERE email = 'system'),
                datetime('now'),
                'UPDATE',
                datetime('now')
            );
        END;
    """)

    op.execute("""
        CREATE TRIGGER IF NOT EXISTS track_instructor_changes
        AFTER UPDATE ON instructors
        BEGIN
            INSERT INTO version_tracking (
                table_name, record_id, version, data, changed_by_id,
                changed_at, change_type, created_at
            )
            VALUES (
                'instructors',
                NEW.id,
                COALESCE((SELECT MAX(version) + 1 FROM version_tracking 
                         WHERE table_name = 'instructors' AND record_id = NEW.id), 1),
                json_object(
                    'id', NEW.id,
                    'user_id', NEW.user_id,
                    'license_number', NEW.license_number,
                    'license_expiry', NEW.license_expiry,
                    'specializations', NEW.specializations
                ),
                (SELECT id FROM users WHERE email = 'system'),
                datetime('now'),
                'UPDATE',
                datetime('now')
            );
        END;
    """)


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS track_instructor_changes;")
    op.execute("DROP TRIGGER IF EXISTS track_student_changes;")
    
    # Drop tables
    op.drop_table('version_conflicts')
    op.drop_table('version_tracking') 