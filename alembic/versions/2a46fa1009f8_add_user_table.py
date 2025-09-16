"""add user table

Revision ID: 2a46fa1009f8
Revises: 8881543cb276
Create Date: 2025-09-15 11:45:20.880903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlmodel import text


# revision identifiers, used by Alembic.
revision: str = '2a46fa1009f8'
down_revision: Union[str, Sequence[str], None] = '8881543cb276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
