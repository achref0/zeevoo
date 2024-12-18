from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '84ee6009ccbb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.alter_column('user_id',
                   existing_type=sa.INTEGER(),
                   nullable=False)
        batch_op.create_unique_constraint('uq_cart_user_id', ['user_id'])


def downgrade():
    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_constraint('uq_cart_user_id', type_='unique')
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

