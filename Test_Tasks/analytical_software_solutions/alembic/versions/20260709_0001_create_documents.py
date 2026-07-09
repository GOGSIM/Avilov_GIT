"""create documents table

Revision ID: 20260709_0001
Revises:
Create Date: 2026-07-09 00:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260709_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rubrics", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_created_date", "documents", ["created_date"])


def downgrade() -> None:
    op.drop_index("ix_documents_created_date", table_name="documents")
    op.drop_table("documents")
