"""empty message

Revision ID: 208a152a6674
Revises: 2d36dd539b2e
Create Date: 2019-12-12 13:09:57.164290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '208a152a6674'
down_revision = '2d36dd539b2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows',
                    'start_time',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    op.drop_column('Venue', 'image_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'Venue',
        sa.Column('image_link',
                  sa.VARCHAR(length=500),
                  autoincrement=False,
                  nullable=True))
    op.alter_column('Shows',
                    'start_time',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    # ### end Alembic commands ###
