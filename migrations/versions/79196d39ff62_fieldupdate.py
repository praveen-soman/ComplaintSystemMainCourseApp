"""fieldupdate

Revision ID: 79196d39ff62
Revises: 18448aa515e3
Create Date: 2023-03-07 20:44:21.057709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '79196d39ff62'
down_revision = '18448aa515e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complaints', sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='state'), server_default='pending', nullable=False))
    op.drop_column('complaints', 'Status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complaints', sa.Column('Status', postgresql.ENUM('pending', 'approved', 'rejected', name='state'), server_default=sa.text("'pending'::state"), autoincrement=False, nullable=False))
    op.drop_column('complaints', 'status')
    # ### end Alembic commands ###
