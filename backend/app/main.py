from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.db.models import Base
from app.db.session import engine
from app.routers import persons as persons_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()

settings = get_settings()
app = FastAPI(title="Genealogy API", version="0.1.0", lifespan=lifespan)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(persons_router.router)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
