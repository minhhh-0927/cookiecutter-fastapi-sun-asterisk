"""create users table

Revision ID: 6d328a456ac4
Revises: 5758d790f1d6
Create Date: 2022-05-20 08:41:48.986129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d328a456ac4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(256), nullable=False),
        sa.Column('hashed_password', sa.String(512), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True)
    )


def downgrade():
    op.drop_table('users')
