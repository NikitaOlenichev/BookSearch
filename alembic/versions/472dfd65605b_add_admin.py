"""add admin

Revision ID: 472dfd65605b
Revises: 93f21ba27f36
Create Date: 2023-04-25 20:13:28.788769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '472dfd65605b'
down_revision = '93f21ba27f36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
