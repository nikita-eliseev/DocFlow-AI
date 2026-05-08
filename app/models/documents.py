from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.status import Status


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4())
    )

    original_filename: Mapped[str] = mapped_column(
        nullable=False
    )

    stored_filename: Mapped[str] = mapped_column(
        nullable=False
    )

    status: Mapped[Status] = mapped_column(
        default=Status.pending,
        index=True
    )

    summary: Mapped[str | None] = mapped_column(
        nullable=True
    )