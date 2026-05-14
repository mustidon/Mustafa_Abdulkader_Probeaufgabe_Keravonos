from datetime import date, time
from typing import Optional

from sqlmodel import Field, SQLModel


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    resource_type: str
    capacity: int
    location: str


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    resource_id: int = Field(foreign_key="resource.id")

    booked_by: str
    title: str

    booking_date: date
    start_time: time
    end_time: time

    note: Optional[str] = None