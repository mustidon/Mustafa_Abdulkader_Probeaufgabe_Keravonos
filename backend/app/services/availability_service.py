from datetime import date, time

from sqlmodel import Session, select

from app.models import Reservation, Resource


def time_ranges_overlap(
    requested_start: time,
    requested_end: time,
    existing_start: time,
    existing_end: time
) -> bool:
    """
    Two bookings overlap when the requested booking starts before an existing
    booking ends and ends after the existing booking starts.
    """
    return requested_start < existing_end and requested_end > existing_start


def reservation_has_conflict(
    session: Session,
    resource_id: int,
    booking_date: date,
    start_time: time,
    end_time: time
) -> bool:
    statement = select(Reservation).where(
        Reservation.resource_id == resource_id,
        Reservation.booking_date == booking_date
    )

    reservations_for_resource = session.exec(statement).all()

    for reservation in reservations_for_resource:
        if time_ranges_overlap(
            requested_start=start_time,
            requested_end=end_time,
            existing_start=reservation.start_time,
            existing_end=reservation.end_time
        ):
            return True

    return False


def get_available_resources(
    session: Session,
    booking_date: date,
    start_time: time,
    end_time: time,
    resource_type: str | None = None
):
    statement = select(Resource)

    if resource_type:
        statement = statement.where(Resource.resource_type == resource_type)

    resources = session.exec(statement).all()
    available_resources = []

    for resource in resources:
        has_conflict = reservation_has_conflict(
            session=session,
            resource_id=resource.id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        )

        if not has_conflict:
            available_resources.append(resource)

    return available_resources