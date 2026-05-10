import time
from app.core.database import SessionLocal
from app.core.status import Status
from app.models.documents import Document
from sqlalchemy import select
from app.utils.pdf import extract_text

def process_documents():
    while True:
        db = SessionLocal()
        
        try:
            stmt = select(Document).where(
                Document.status == Status.pending
            )
            
            document = db.execute(stmt).scalars().first()
            
            if document:
                print(f"Processing: {document.id}")
                
                document.status = Status.processing
                
                db.commit()
                
                ###
                time.sleep(5)
                
                file_path = f"uploads/{document.stored_filename}"
                text = extract_text(file_path=file_path)
                document.summary = text[:500]
                
                document.status = Status.completed
                
                db.commit()
                
                print(f"Completed: {document.id}")

            else:
                print("No pending documents")
                
        finally:
            db.close()
            
        time.sleep(3)
        
if __name__ == "__main__":
    process_documents()