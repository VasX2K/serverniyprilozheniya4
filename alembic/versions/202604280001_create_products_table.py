"""create products table

Revision ID: 202604280001
Revises:
Create Date: 2026-04-28 12:45:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202604280001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_title"), "products", ["title"], unique=False)

    products = sa.table(
        "products",
        sa.column("id", sa.Integer),
        sa.column("title", sa.String),
        sa.column("price", sa.Float),
        sa.column("count", sa.Integer),
    )
    op.bulk_insert(
        products,
        [
            {"id": 1, "title": "Mechanical keyboard", "price": 7990.0, "count": 12},
            {"id": 2, "title": "Wireless mouse", "price": 2490.0, "count": 25},
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_products_title"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")

