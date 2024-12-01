"""add rsvp date

Revision ID: 13fe16594d5b
Revises: 0b404e81d758
Create Date: 2024-12-01 19:08:17.669295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '13fe16594d5b'
down_revision: Union[str, None] = '0b404e81d758'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rsvps', sa.Column('rsvp_date', postgresql.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rsvps', 'rsvp_date')
    # ### end Alembic commands ###
