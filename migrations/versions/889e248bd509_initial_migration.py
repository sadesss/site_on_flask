"""initial migration

Revision ID: 889e248bd509
Revises: 1f3c9c08f5d9
Create Date: 2023-12-25 16:41:45.776173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '889e248bd509'
down_revision = '1f3c9c08f5d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###