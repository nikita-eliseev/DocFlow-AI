import shutil
from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter(tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload")
async def upload_pdf(file: Annotated[UploadFile, File(...)]):
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid4()}{ext}"
    
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "original_filename": file.filename,
        "stored_filename": unique_name,
        "status": "uploaded"
    }