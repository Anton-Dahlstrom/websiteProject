"""create api update table

Revision ID: b3cbf224fd61
Revises: d528d5e7b11c
Create Date: 2023-10-21 22:54:47.102080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3cbf224fd61'
down_revision: Union[str, None] = 'd528d5e7b11c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("updates",
            sa.Column("updated", sa.DateTime(), primary_key=True, nullable=False),
            sa.Column("next_update", sa.DateTime(), nullable=False),
            sa.Column("api_source", sa.String()))


def downgrade() -> None:
    op.drop_table("updates")
