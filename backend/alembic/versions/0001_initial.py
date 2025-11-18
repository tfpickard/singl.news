from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "story_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("full_text", sa.Text(), nullable=False),
        sa.Column("summary", sa.String(length=1024), nullable=False),
        sa.Column("context_summary", sa.Text(), nullable=True),
        sa.Column("sources_snapshot", sa.JSON(), nullable=True),
        sa.Column("token_stats", sa.JSON(), nullable=True),
    )
    op.create_index("ix_story_versions_created_at", "story_versions", ["created_at"])

    op.create_table(
        "feed_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("feed_url", sa.String(length=512), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("link", sa.String(length=512), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("hash", sa.String(length=512), nullable=False),
        sa.Column("raw", sa.JSON(), nullable=True),
        sa.Column("story_version_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["story_version_id"], ["story_versions.id"], ondelete="SET NULL"),
    )
    op.create_unique_constraint("uq_feed_items_hash", "feed_items", ["hash"])


def downgrade() -> None:
    op.drop_table("feed_items")
    op.drop_table("story_versions")
