"""create local_uploads table

Revision ID: 2803c57a22f2
Revises: 6d328a456ac4
Create Date: 2022-05-25 10:42:19.721339

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '2803c57a22f2'
down_revision = '6d328a456ac4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'local_uploads',
        sa.Column('id', UUID, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('filename', sa.String(256), unique=True, index=True, nullable=False),
        sa.Column('filesize', sa.Float, default=0.0),
        sa.Column('filepath', sa.String(256), nullable=False),
        sa.Column('created_on', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_on', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('del_flag', sa.Boolean, default=True),

    )


def downgrade():
    op.drop_table('local_uploads')
