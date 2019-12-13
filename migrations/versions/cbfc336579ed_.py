"""empty message

Revision ID: cbfc336579ed
Revises: e6f29a043725
Create Date: 2019-12-12 11:11:28.843531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbfc336579ed'
down_revision = 'e6f29a043725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_column('Shows', 'artist_id')
    # ### end Alembic commands ###
