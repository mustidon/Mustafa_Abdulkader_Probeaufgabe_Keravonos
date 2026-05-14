from datetime import date, time
from typing import Optional

from pydantic import BaseModel, field_validator


class ResourceRead(BaseModel):
    id: int
    name: str
    resource_type: str
    capacity: int
    location: str


class ReservationCreate(BaseModel):
    resource_id: int
    booked_by: str
    title: str
    booking_date: date
    start_time: time
    end_time: time
    note: Optional[str] = None

    @field_validator("booked_by", "title")
    @classmethod
    def text_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be empty.")
        return value.strip()

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, end_time, info):
        start_time = info.data.get("start_time")

        if start_time and end_time <= start_time:
            raise ValueError("End time must be after start time.")

        return end_time


class ReservationRead(BaseModel):
    id: int
    resource_id: int
    booked_by: str
    title: str
    booking_date: date
    start_time: time
    end_time: time
    note: Optional[str] = None