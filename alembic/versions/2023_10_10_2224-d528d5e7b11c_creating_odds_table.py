"""creating odds table

Revision ID: d528d5e7b11c
Revises: a734bc11412b
Create Date: 2023-10-10 22:24:20.726998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd528d5e7b11c'
down_revision: Union[str, None] = 'a734bc11412b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("odds",
            sa.Column("id", sa.String(), nullable=False, primary_key=True),
            sa.Column("sport_title", sa.String(), nullable=False),
            sa.Column("commence_time", sa.DateTime(), nullable=False),
            sa.Column("home_team", sa.String(), nullable=False),
            sa.Column("away_team", sa.String(), nullable=False),          
            sa.Column("home_odds", sa.Float(), nullable=True),
            sa.Column("away_odds", sa.Float(), nullable=True),
            sa.Column("draw_odds", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_table("odds")
