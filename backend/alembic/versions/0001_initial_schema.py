"""Initial database schema creating users and scans tables

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-07-28 19:42:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 2. Create scans table
    op.create_table(
        'scans',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('payload_type', sa.String(length=50), nullable=False),
        sa.Column('raw_content', sa.Text(), nullable=False),
        sa.Column('anonymized_content', sa.Text(), nullable=True),
        sa.Column('threat_score', sa.Integer(), nullable=False),
        sa.Column('risk_band', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.95'),
        sa.Column('rationale_summary', sa.Text(), nullable=False),
        sa.Column('detected_manipulations', sa.Text(), nullable=True),
        sa.Column('suspicious_urls', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scans_id'), 'scans', ['id'], unique=False)
    op.create_index(op.f('ix_scans_user_id'), 'scans', ['user_id'], unique=False)
    op.create_index(op.f('ix_scans_payload_type'), 'scans', ['payload_type'], unique=False)
    op.create_index(op.f('ix_scans_threat_score'), 'scans', ['threat_score'], unique=False)
    op.create_index(op.f('ix_scans_risk_band'), 'scans', ['risk_band'], unique=False)
    op.create_index(op.f('ix_scans_created_at'), 'scans', ['created_at'], unique=False)

def downgrade() -> None:
    # Drop tables in reverse dependency order
    op.drop_index(op.f('ix_scans_created_at'), table_name='scans')
    op.drop_index(op.f('ix_scans_risk_band'), table_name='scans')
    op.drop_index(op.f('ix_scans_threat_score'), table_name='scans')
    op.drop_index(op.f('ix_scans_payload_type'), table_name='scans')
    op.drop_index(op.f('ix_scans_user_id'), table_name='scans')
    op.drop_index(op.f('ix_scans_id'), table_name='scans')
    op.drop_table('scans')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
