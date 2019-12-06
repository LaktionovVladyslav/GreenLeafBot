"""create orders table

Revision ID: 9c7d5c199e4f
Revises: e3b3df2f2ce7
Create Date: 2019-12-06 01:05:11.862122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7d5c199e4f'
down_revision = 'e3b3df2f2ce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('orders_status_fkey', 'orders', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('orders_status_fkey', 'orders', 'plant_culture', ['status'], ['id'])
    # ### end Alembic commands ###