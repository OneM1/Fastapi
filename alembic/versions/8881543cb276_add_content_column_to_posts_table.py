"""add content column to posts table

Revision ID: 8881543cb276
Revises: b7660bf36589
Create Date: 2025-09-15 11:39:57.429307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8881543cb276'
down_revision: Union[str, Sequence[str], None] = 'b7660bf36589'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
