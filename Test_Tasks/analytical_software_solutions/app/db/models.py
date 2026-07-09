from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (Index("ix_documents_created_date", "created_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rubrics: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
