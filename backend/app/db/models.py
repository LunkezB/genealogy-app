from datetime import date

from sqlalchemy import String, Integer, Text, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "persons"

    sosa: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    death: Mapped[date | None] = mapped_column(Date, nullable=True)
    place: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
