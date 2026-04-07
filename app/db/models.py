from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


class ArbitrDoc(Base):
    __tablename__ = "arbitr_docs"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_number: Mapped[str] = mapped_column(String, index=True)
    last_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    document_name: Mapped[str] = mapped_column(String, nullable=True)
    parsed_at: Mapped[DateTime] = mapped_column(default=datetime.utcnow)
