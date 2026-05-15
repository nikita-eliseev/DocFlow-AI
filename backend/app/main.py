from fastapi import FastAPI
from app.api.routes.documents import router as docs_router
from app.core.config import settings

app = FastAPI(
    title="DOCFLOW-AI",
    debug=settings.debug
)

app.include_router(docs_router)