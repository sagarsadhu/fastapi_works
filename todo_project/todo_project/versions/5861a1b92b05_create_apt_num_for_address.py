"""create apt_num for address

Revision ID: 5861a1b92b05
Revises: 8c7390077556
Create Date: 2022-10-28 10:29:30.039785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5861a1b92b05'
down_revision = '8c7390077556'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
