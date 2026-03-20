from fastapi import FastAPI

from app.api.routes.user import router as user_router
from app.core.config import settings
from app.core.database import Base, engine

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {
        "message": "API is running",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
