"""change books

Revision ID: ffff9549af3c
Revises: 97ee7c494de5
Create Date: 2023-04-23 18:44:47.592674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffff9549af3c'
down_revision = '97ee7c494de5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('orig_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'orig_name')
    # ### end Alembic commands ###
