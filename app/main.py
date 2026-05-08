from fastapi import FastAPI
from app.api.routes.documents import router as docs_router

app = FastAPI()

app.include_router(docs_router)