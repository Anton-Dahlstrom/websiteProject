"""add email to user table

Revision ID: a734bc11412b
Revises: 2dff66a84039
Create Date: 2023-10-09 21:26:17.982241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a734bc11412b'
down_revision: Union[str, None] = '2dff66a84039'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", 
                  sa.Column("email", sa.String(), nullable=True, unique=True))


def downgrade() -> None:
    op.drop_column("users", "email")
    pass
