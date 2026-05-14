from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Reservation, Resource
from app.schemas import ReservationCreate, ReservationRead
from app.services.availability_service import reservation_has_conflict


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("", response_model=list[ReservationRead])
def list_reservations(
    booking_date: Optional[date] = None,
    session: Session = Depends(get_session)
):
    statement = select(Reservation)

    if booking_date:
        statement = statement.where(Reservation.booking_date == booking_date)

    reservations = session.exec(statement).all()
    return reservations


@router.post(
    "",
    response_model=ReservationRead,
    status_code=status.HTTP_201_CREATED
)
def create_reservation(
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session)
):
    resource = session.get(Resource, reservation_data.resource_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found."
        )

    has_conflict = reservation_has_conflict(
        session=session,
        resource_id=reservation_data.resource_id,
        booking_date=reservation_data.booking_date,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time
    )

    if has_conflict:
        raise HTTPException(
            status_code=409,
            detail="This resource is already booked during the selected time."
        )

    reservation = Reservation(**reservation_data.model_dump())

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    session: Session = Depends(get_session)
):
    reservation = session.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found."
        )

    session.delete(reservation)
    session.commit()