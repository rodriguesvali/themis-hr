"""Add message review metadata

Revision ID: 8b9f2d4c1a3e
Revises: 19a2612a75de
Create Date: 2026-04-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b9f2d4c1a3e"
down_revision: Union[str, Sequence[str], None] = "19a2612a75de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("messages", sa.Column("category", sa.String(), nullable=True))
    op.add_column("messages", sa.Column("specialist", sa.String(), nullable=True))
    op.add_column("messages", sa.Column("confidence", sa.String(), nullable=True))
    op.add_column("messages", sa.Column("escalation_reason", sa.Text(), nullable=True))
    op.add_column(
        "messages",
        sa.Column("legal_reviewed", sa.Boolean(), nullable=True, server_default=sa.false()),
    )
    op.add_column("messages", sa.Column("legal_risk_level", sa.String(), nullable=True))
    op.add_column("messages", sa.Column("legal_notes", sa.Text(), nullable=True))
    op.add_column("messages", sa.Column("legal_basis", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("messages", "legal_basis")
    op.drop_column("messages", "legal_notes")
    op.drop_column("messages", "legal_risk_level")
    op.drop_column("messages", "legal_reviewed")
    op.drop_column("messages", "escalation_reason")
    op.drop_column("messages", "confidence")
    op.drop_column("messages", "specialist")
    op.drop_column("messages", "category")
