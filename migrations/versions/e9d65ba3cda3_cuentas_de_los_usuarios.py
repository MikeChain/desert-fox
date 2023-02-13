"""Cuentas de los usuarios

Revision ID: e9d65ba3cda3
Revises: cc40fc3bdf4c
Create Date: 2023-02-12 17:16:53.078523

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e9d65ba3cda3"
down_revision = "cc40fc3bdf4c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=25), nullable=False),
        sa.Column(
            "account_type",
            sa.Enum("cash", "debit", "credit", name="account_type"),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.Enum("MXN", "USD", "EUR", name="currency_id"),
            server_default="MXN",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("initial_balance", sa.DECIMAL(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.create_index(
            "accounts_user_id_index", ["user_id"], unique=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("accounts", schema=None) as batch_op:
        batch_op.drop_index("accounts_user_id_index")

    op.drop_table("accounts")

    op.execute("DROP TYPE account_type;")
    op.execute("DROP TYPE currency_id;")
    # ### end Alembic commands ###
