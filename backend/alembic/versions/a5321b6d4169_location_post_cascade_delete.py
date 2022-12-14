"""location post cascade delete

Revision ID: a5321b6d4169
Revises: 238bb2a0525e
Create Date: 2022-09-01 11:00:24.116705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5321b6d4169'
down_revision = '238bb2a0525e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_location_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'locations', ['location_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_location_id_fkey', 'posts', 'locations', ['location_id'], ['id'])
    # ### end Alembic commands ###
