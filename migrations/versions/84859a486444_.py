"""empty message

Revision ID: 84859a486444
Revises: 685d37e9fdcb
Create Date: 2019-12-11 14:45:34.265327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84859a486444'
down_revision = '685d37e9fdcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_name', sa.String(length=120), nullable=True),
    sa.Column('artist_name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Shows')
    # ### end Alembic commands ###
