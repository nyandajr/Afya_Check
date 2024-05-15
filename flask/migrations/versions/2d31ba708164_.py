"""empty message

Revision ID: 2d31ba708164
Revises: 39490f396c55
Create Date: 2023-10-20 08:48:47.073126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d31ba708164'
down_revision = '39490f396c55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment_option', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment_option', schema=None) as batch_op:
        batch_op.drop_column('value')

    # ### end Alembic commands ###
