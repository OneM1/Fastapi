"""add last few columns to posts table

Revision ID: 2c9d76045ec1
Revises: 7b3265c1a32b
Create Date: 2025-09-15 12:00:13.479246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlmodel import text


# revision identifiers, used by Alembic.
revision: str = '2c9d76045ec1'
down_revision: Union[str, Sequence[str], None] = '7b3265c1a32b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column("published", sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('posts', sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        nullable=False
    ))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
