"""create account and transaction tables

Revision ID: 19378cd6280b
Revises:
Create Date: 2021-03-27 08:13:30.680894

"""
from sqlalchemy import Column, ForeignKey, Integer, String

from alembic import op

# revision identifiers, used by Alembic.
revision = "19378cd6280b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "accounts",
        Column("id", String, primary_key=True, nullable=False),
        Column("name", String, nullable=False),
    )

    op.create_table(
        "transactions",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("from_account_id", String, ForeignKey("accounts.id"), nullable=False),
        Column("to_account_id", String, ForeignKey("accounts.id"), nullable=False),
        Column("quantity", Integer, nullable=False),
    )


def downgrade():
    op.drop_table("accounts")
    op.drop_table("transactions")
