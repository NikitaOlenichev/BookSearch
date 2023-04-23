"""change books

Revision ID: 97ee7c494de5
Revises: c45539f422ab
Create Date: 2023-04-23 15:25:28.466501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97ee7c494de5'
down_revision = 'c45539f422ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('comments', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'comments')
    # ### end Alembic commands ###
