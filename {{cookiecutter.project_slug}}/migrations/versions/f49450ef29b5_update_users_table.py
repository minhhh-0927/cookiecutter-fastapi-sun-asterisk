"""update users table

Revision ID: f49450ef29b5
Revises: 2803c57a22f2
Create Date: 2022-05-26 09:59:20.803385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f49450ef29b5'
down_revision = '2803c57a22f2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
        sa.Column('created_on', sa.DateTime, default=sa.func.now())
    )
    op.add_column('users',
        sa.Column('updated_on', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    op.add_column('users',
        sa.Column('del_flag', sa.Boolean, default=True)
    )


def downgrade():
    op.drop_column('users', 'created_on')
    op.drop_column('users', 'updated_on')
    op.drop_column('users', 'del_flag')
