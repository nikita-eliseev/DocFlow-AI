from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies.db import get_document_service
from app.schemas.documents import DocumentResponse

from app.services.documents import DocService

router = APIRouter(prefix="documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    documents_service: DocService = Depends(get_document_service)
):
    return documents_service.up_doc(file=file)
