from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[str] = mapped_column(server_default="now()")
    updated_at: Mapped[str] = mapped_column(server_default="now()", onupdate="now()")
