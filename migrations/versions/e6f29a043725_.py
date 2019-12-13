"""empty message

Revision ID: e6f29a043725
Revises: 46f3aa839fdf
Create Date: 2019-12-12 10:54:13.831289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6f29a043725'
down_revision = '46f3aa839fdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.drop_column('Shows', 'venue_name')
    op.drop_column('Shows', 'artist_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Shows', sa.Column('venue_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_column('Shows', 'venue_id')
    # ### end Alembic commands ###