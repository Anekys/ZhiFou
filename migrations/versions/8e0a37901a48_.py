"""empty message

Revision ID: 8e0a37901a48
Revises: e625d15afb7b
Create Date: 2022-09-01 10:13:24.451729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e0a37901a48'
down_revision = 'e625d15afb7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'create_time')
    # ### end Alembic commands ###