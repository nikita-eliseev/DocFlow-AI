import shutil
from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File
import os
from app.core.dependencies import get_db
from app.models.documents import Document
from app.schemas.documents import DocumentResponse
from sqlalchemy.orm import Session

router = APIRouter(tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_pdf(
    file: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid4()}{ext}"
    
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    document = Document(
        original_filename = file.filename,
        stored_filename = unique_name
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document
