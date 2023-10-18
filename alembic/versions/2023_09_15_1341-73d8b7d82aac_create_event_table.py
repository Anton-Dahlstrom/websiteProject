"""create event table

Revision ID: 73d8b7d82aac
Revises: 
Create Date: 2023-09-15 13:41:46.204527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73d8b7d82aac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("events",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("created_time", sa.TIMESTAMP(timezone=True), nullable=False, 
                              server_default=sa.text('NOW()')),
                    sa.Column("hometeam", sa.String(), nullable=False),
                    sa.Column("awayteam", sa.String(), nullable=False),
                    sa.Column("date", sa.DateTime(), nullable=False))
def downgrade() -> None:
    op.drop_table("events")
    pass
