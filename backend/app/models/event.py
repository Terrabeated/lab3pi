from sqlalchemy import Integer, String, TIMESTAMP
from datetime import date as date_type

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ..config.db import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    date: Mapped[date_type]= mapped_column(TIMESTAMP, nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)