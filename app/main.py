from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes.documents import router as docs_router
from app.core.database import Base
from app.core.database import engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(docs_router)