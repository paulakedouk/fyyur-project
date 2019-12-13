"""empty message

Revision ID: 7683faf1e1f1
Revises: 3fff90733a9e
Create Date: 2019-12-11 15:21:30.726681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7683faf1e1f1'
down_revision = '3fff90733a9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
