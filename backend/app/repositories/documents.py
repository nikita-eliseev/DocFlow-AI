from sqlalchemy.orm import Session
from sqlalchemy import select
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
    
    def get_by_id(self, document_id: str) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)
        return self.db.execute(stmt).scalars().first()
    
    def get_all(self) -> list[Document]:
        stmt = select(Document)
        return list(
            self.db.execute(stmt).scalars().all()
        )