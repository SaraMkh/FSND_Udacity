"""empty message

Revision ID: 8574d4ccf8a0
Revises: 10918c8a2e0e
Create Date: 2020-10-21 23:01:06.844801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8574d4ccf8a0'
down_revision = '10918c8a2e0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
