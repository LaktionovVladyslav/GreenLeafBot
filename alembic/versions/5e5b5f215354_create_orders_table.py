"""create orders table

Revision ID: 5e5b5f215354
Revises: 9c2dbd5bfa98
Create Date: 2019-12-06 00:57:56.024207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e5b5f215354'
down_revision = '9c2dbd5bfa98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint('orders_status_fkey', 'orders', type_='foreignkey')
    op.drop_column('orders', 'order_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_foreign_key('orders_status_fkey', 'orders', 'plant_culture', ['status'], ['id'])
    op.drop_column('orders', 'id')
    # ### end Alembic commands ###
