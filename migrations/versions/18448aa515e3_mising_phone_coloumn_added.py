"""mising phone coloumn added

Revision ID: 18448aa515e3
Revises: bd386d4f5d39
Create Date: 2023-03-01 14:18:28.878722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18448aa515e3'
down_revision = 'bd386d4f5d39'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
