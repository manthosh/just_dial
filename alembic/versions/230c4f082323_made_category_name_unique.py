"""Made category name unique

Revision ID: 230c4f082323
Revises: 290322df8cdd
Create Date: 2014-10-12 02:38:03.509408

"""

# revision identifiers, used by Alembic.
revision = '230c4f082323'
down_revision = '290322df8cdd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'category', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category')
    ### end Alembic commands ###
