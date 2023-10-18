"""create user table

Revision ID: 2dff66a84039
Revises: 73d8b7d82aac
Create Date: 2023-09-23 11:13:53.836747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dff66a84039'
down_revision: Union[str, None] = '73d8b7d82aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                sa.Column("created_time", sa.TIMESTAMP(timezone=True), nullable=False, 
                            server_default=sa.text('NOW()')),
                sa.Column("username", sa.String(), nullable=False, unique=True),
                sa.Column("password", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("users")
