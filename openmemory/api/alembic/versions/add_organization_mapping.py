"""add organization support

Revision ID: add_organization_mapping
Revises: afd00efbd06b
Create Date: 2025-06-30 00:00:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'add_organization_mapping'
down_revision: Union[str, None] = 'afd00efbd06b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'organizations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('organization_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_organization_id'), 'organizations', ['organization_id'], unique=True)
    op.create_index(op.f('ix_organizations_created_at'), 'organizations', ['created_at'], unique=False)
    op.add_column('users', sa.Column('organization_id', sa.UUID(), nullable=False, server_default='00000000-0000-0000-0000-000000000000'))
    op.create_foreign_key(None, 'users', 'organizations', ['organization_id'], ['id'])
    op.create_unique_constraint('idx_user_org', 'users', ['user_id', 'organization_id'])
    op.alter_column('users', 'organization_id', server_default=None)


def downgrade() -> None:
    op.drop_constraint('idx_user_org', 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'organization_id')
    op.drop_index(op.f('ix_organizations_organization_id'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_created_at'), table_name='organizations')
    op.drop_table('organizations')
