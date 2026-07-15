"""create appointment engine

Revision ID: 20260715_0002
Revises: 20260714_0001
Create Date: 2026-07-15
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260715_0002"
down_revision: str | None = "20260714_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "doctors",
        sa.Column("status", sa.String(length=50), server_default="active", nullable=False),
    )
    op.add_column(
        "doctors",
        sa.Column(
            "work_start_time",
            sa.Time(),
            server_default=sa.text("'09:00:00'"),
            nullable=False,
        ),
    )
    op.add_column(
        "doctors",
        sa.Column(
            "work_end_time",
            sa.Time(),
            server_default=sa.text("'17:00:00'"),
            nullable=False,
        ),
    )

    op.add_column(
        "appointments",
        sa.Column("patient_phone", sa.String(length=40), nullable=True),
    )
    op.add_column(
        "appointments",
        sa.Column("reason_for_visit", sa.String(length=500), nullable=True),
    )
    op.add_column(
        "appointments",
        sa.Column("appointment_date", sa.Date(), nullable=True),
    )
    op.add_column(
        "appointments",
        sa.Column("appointment_start_time", sa.Time(), nullable=True),
    )
    op.add_column(
        "appointments",
        sa.Column("appointment_end_time", sa.Time(), nullable=True),
    )
    op.add_column("appointments", sa.Column("notes", sa.Text(), nullable=True))

    bind = op.get_bind()
    op.execute("UPDATE appointments SET status = 'pending' WHERE status = 'draft'")
    op.execute("UPDATE appointments SET patient_phone = 'unknown' WHERE patient_phone IS NULL")
    op.execute(
        "UPDATE appointments SET reason_for_visit = 'Not specified' "
        "WHERE reason_for_visit IS NULL"
    )
    if bind.dialect.name == "postgresql":
        op.execute(
            "UPDATE appointments SET appointment_date = CAST(scheduled_at AS DATE) "
            "WHERE appointment_date IS NULL"
        )
        op.execute(
            "UPDATE appointments SET appointment_start_time = CAST(scheduled_at AS TIME) "
            "WHERE appointment_start_time IS NULL"
        )
        op.execute(
            "UPDATE appointments SET appointment_end_time = "
            "CAST(scheduled_at + INTERVAL '30 minutes' AS TIME) "
            "WHERE appointment_end_time IS NULL"
        )

    op.alter_column("appointments", "patient_email", nullable=False)
    op.alter_column("appointments", "doctor_id", nullable=False)
    op.alter_column("appointments", "department_id", nullable=False)
    op.alter_column("appointments", "patient_phone", nullable=False)
    op.alter_column("appointments", "reason_for_visit", nullable=False)
    op.alter_column("appointments", "appointment_date", nullable=False)
    op.alter_column("appointments", "appointment_start_time", nullable=False)
    op.alter_column("appointments", "appointment_end_time", nullable=False)
    op.drop_column("appointments", "scheduled_at")


def downgrade() -> None:
    op.add_column(
        "appointments",
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.drop_column("appointments", "notes")
    op.drop_column("appointments", "appointment_end_time")
    op.drop_column("appointments", "appointment_start_time")
    op.drop_column("appointments", "appointment_date")
    op.drop_column("appointments", "reason_for_visit")
    op.drop_column("appointments", "patient_phone")

    op.drop_column("doctors", "work_end_time")
    op.drop_column("doctors", "work_start_time")
    op.drop_column("doctors", "status")
