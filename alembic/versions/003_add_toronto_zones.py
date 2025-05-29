"""Add Toronto zones

Revision ID: 003
Revises: 002
Create Date: 2024-03-20 10:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create zones table
    op.create_table(
        'zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create zone_boundaries table
    op.create_table(
        'zone_boundaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('sequence', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create instructor_zones table
    op.create_table(
        'instructor_zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
        sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create lesson_zones table
    op.create_table(
        'lesson_zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('lesson_zones')
    op.drop_table('instructor_zones')
    op.drop_table('zone_boundaries')
    op.drop_table('zones') 