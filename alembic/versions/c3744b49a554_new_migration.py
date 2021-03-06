"""New Migration

Revision ID: c3744b49a554
Revises: 0967d398fe1b
Create Date: 2021-08-08 15:27:20.170761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3744b49a554'
down_revision = '0967d398fe1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('unit_of_currency', sa.String(), nullable=True))
    op.add_column('book', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'price')
    op.drop_column('book', 'unit_of_currency')
    # ### end Alembic commands ###
