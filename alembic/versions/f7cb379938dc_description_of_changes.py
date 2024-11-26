"""description of changes

Revision ID: f7cb379938dc
Revises: f9b7d319f204
Create Date: 2024-11-25 22:00:18.983233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cb379938dc'
down_revision: Union[str, None] = 'f9b7d319f204'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_admins_id', table_name='admins')
    op.drop_table('admins')
    op.drop_index('ix_items_id', table_name='items')
    op.drop_table('items')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('image_path', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_index('ix_items_id', 'items', ['id'], unique=False)
    op.create_table('admins',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='admins_pkey'),
    sa.UniqueConstraint('username', name='admins_username_key')
    )
    op.create_index('ix_admins_id', 'admins', ['id'], unique=False)
    # ### end Alembic commands ###
