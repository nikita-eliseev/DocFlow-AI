import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.repositories.documents import DocRepository
from app.schemas.documents import DocumentResponse


class DocService:
    def __init__(self, db: Session):
        self.db = db
        self.docrepository = DocRepository(db)

    def up_doc(self, file: UploadFile) -> DocumentResponse:
        
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid4()}{ext}"

        file_path = os.path.join("uploads", unique_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = self.docrepository.create(
            original_filename=file.filename,
            stored_filename=unique_name
        )

        self.db.commit()
        self.db.refresh(document)

        return DocumentResponse.model_validate(document)
        
        
        
        