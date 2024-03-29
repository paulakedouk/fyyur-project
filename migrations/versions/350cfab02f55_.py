"""empty message

Revision ID: 350cfab02f55
Revises: fef43bfa92dc
Create Date: 2019-12-13 14:09:51.503921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '350cfab02f55'
down_revision = 'fef43bfa92dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
