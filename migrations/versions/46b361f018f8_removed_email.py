"""Removed email

Revision ID: 46b361f018f8
Revises: c5c6b1cc32c7
Create Date: 2024-03-31 11:42:54.753354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b361f018f8'
down_revision = 'c5c6b1cc32c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_email')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=64), nullable=False))
        batch_op.create_index('ix_user_email', ['email'], unique=1)

    # ### end Alembic commands ###
