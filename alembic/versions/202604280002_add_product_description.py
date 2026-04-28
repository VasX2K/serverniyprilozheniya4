"""add product description

Revision ID: 202604280002
Revises: 202604280001
Create Date: 2026-04-28 12:50:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202604280002"
down_revision: Union[str, None] = "202604280001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "description",
                sa.String(length=500),
                nullable=False,
                server_default="Description will be filled later",
            )
        )

    op.execute(
        "UPDATE products SET description = 'Compact keyboard for everyday development' "
        "WHERE title = 'Mechanical keyboard'"
    )
    op.execute(
        "UPDATE products SET description = 'Ergonomic mouse for office work' "
        "WHERE title = 'Wireless mouse'"
    )


def downgrade() -> None:
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("description")

