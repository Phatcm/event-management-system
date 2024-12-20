"""add_rsvp_relations

Revision ID: 0b404e81d758
Revises: faec87c2c089
Create Date: 2024-12-01 18:19:51.428550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0b404e81d758'
down_revision: Union[str, None] = 'faec87c2c089'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rsvps',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('user_uid', sa.Uuid(), nullable=False),
    sa.Column('event_uid', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['event_uid'], ['events.uid'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rsvps')
    # ### end Alembic commands ###
