from sqlalchemy.orm import Session

from app.models.documents import Document

class DocRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, original_filename: str, stored_filename: str) -> Document:
        document = Document(
            original_filename=original_filename,
            stored_filename=stored_filename
        )

        self.db.add(document)
        self.db.flush()  

        return document