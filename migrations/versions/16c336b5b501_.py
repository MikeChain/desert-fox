"""empty message

Revision ID: 16c336b5b501
Revises: 000ffa17f825
Create Date: 2023-02-18 22:26:53.788423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c336b5b501'
down_revision = '000ffa17f825'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_accounts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('account_id', sa.UUID(), nullable=True),
    sa.Column('transaction_id', sa.UUID(), nullable=True),
    sa.Column('subtotal_amount', sa.Numeric(precision=20, scale=4), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('payment_accounts', schema=None) as batch_op:
        batch_op.create_index('account_index', ['account_id'], unique=False)
        batch_op.create_index('transaction_account_index', ['transaction_id'], unique=False)

    op.create_table('transaction_details_model',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('transaction_id', sa.UUID(), nullable=True),
    sa.Column('subcategory_id', sa.UUID(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Numeric(precision=20, scale=4), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('transaction_details_model', schema=None) as batch_op:
        batch_op.create_index('subcategory_details_index', ['subcategory_id'], unique=False)
        batch_op.create_index('transaction_details_index', ['transaction_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_details_model', schema=None) as batch_op:
        batch_op.drop_index('transaction_details_index')
        batch_op.drop_index('subcategory_details_index')

    op.drop_table('transaction_details_model')
    with op.batch_alter_table('payment_accounts', schema=None) as batch_op:
        batch_op.drop_index('transaction_account_index')
        batch_op.drop_index('account_index')

    op.drop_table('payment_accounts')
    # ### end Alembic commands ###