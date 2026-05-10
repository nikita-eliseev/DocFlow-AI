from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.documents import DocService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_document_service(db: Session = Depends(get_db)):
    return DocService(db=db)