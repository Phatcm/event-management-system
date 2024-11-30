from fastapi import FastAPI
from src.events.routes import event_router
from contextlib import asynccontextmanager
from src.db.main import init_db


# Define lifespan event for task that require it
@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server has been stopped.")


# App configuration
version = "v1"

app = FastAPI(
    title="Event Management",
    description="A REST API for a event management service",
    version=version,
    lifespan=life_span,
)

app.include_router(event_router, prefix=f"/api/{version}/events", tags=["events"])
