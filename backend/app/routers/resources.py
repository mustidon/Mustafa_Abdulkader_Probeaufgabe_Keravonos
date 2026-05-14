from datetime import date, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Resource
from app.schemas import ResourceRead
from app.services.availability_service import get_available_resources


router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("", response_model=list[ResourceRead])
def list_resources(session: Session = Depends(get_session)):
    statement = select(Resource)
    resources = session.exec(statement).all()
    return resources


@router.get("/available", response_model=list[ResourceRead])
def list_available_resources(
    booking_date: date,
    start_time: time,
    end_time: time,
    resource_type: Optional[str] = None,
    session: Session = Depends(get_session)
):
    if end_time <= start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time."
        )

    if resource_type and resource_type not in ["room", "desk"]:
        raise HTTPException(
            status_code=400,
            detail="Resource type must be 'room' or 'desk'."
        )

    return get_available_resources(
        session=session,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        resource_type=resource_type
    )