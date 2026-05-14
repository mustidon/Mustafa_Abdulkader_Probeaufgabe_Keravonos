from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.database import create_db_and_tables, engine
from app.routers.resources import router as resources_router
from app.routers.reservations import router as reservations_router
from app.seed import seed_resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    with Session(engine) as session:
        seed_resources(session)

    yield


app = FastAPI(
    title="Office Booking API",
    description="API for booking rooms and flexible desks in a small office.",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resources_router)
app.include_router(reservations_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Office Booking API is running."
    }