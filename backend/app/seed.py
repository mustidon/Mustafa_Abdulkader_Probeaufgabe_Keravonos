from sqlmodel import Session, select

from app.models import Resource


def seed_resources(session: Session):
    existing_resource = session.exec(select(Resource)).first()

    if existing_resource:
        return

    resources = [
        Resource(
            name="Meetingraum A",
            resource_type="room",
            capacity=8,
            location="1. Etage"
        ),
        Resource(
            name="Meetingraum B",
            resource_type="room",
            capacity=4,
            location="1. Etage"
        ),
        Resource(
            name="Arbeitsplatz 1",
            resource_type="desk",
            capacity=1,
            location="Open Space"
        ),
        Resource(
            name="Arbeitsplatz 2",
            resource_type="desk",
            capacity=1,
            location="Open Space"
        ),
        Resource(
            name="Arbeitsplatz 3",
            resource_type="desk",
            capacity=1,
            location="Open Space"
        ),
    ]

    session.add_all(resources)
    session.commit()