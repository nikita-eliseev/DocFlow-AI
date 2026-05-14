from app.core.celery import celery_app
from app.core.database import SessionLocal
from app.core.status import Status
from app.models.documents import Document
from sqlalchemy import select
from app.utils.pdf import extract_text
from app.core.loger import logger
from app.core.locks import acquire_lock, release_lock
from pathlib import Path


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_document(self, document_id: str):
    db = SessionLocal()

    lock_key = f"doc-lock:{document_id}"

    logger.info(
        "task_started",
        extra={"document_id": document_id, "task_id": self.request.id},
    )

    try:
        if not acquire_lock(lock_key, ttl=300):
            logger.warning(
                "lock_not_acquired",
                extra={"document_id": document_id},
            )
            return None

        logger.info(
            "lock_acquired",
            extra={"document_id": document_id},
        )

        stmt = select(Document).where(Document.id == document_id)
        document = db.execute(stmt).scalars().first()

        if not document:
            logger.warning(
                "document_not_found",
                extra={"document_id": document_id},
            )
            return None

        logger.info(
            "document_loaded",
            extra={
                "document_id": document_id,
                "status": document.status,
            },
        )

        if document.status != Status.pending:
            logger.info(
                "document_skipped_wrong_status",
                extra={
                    "document_id": document_id,
                    "status": document.status,
                },
            )
            return None

        document.status = Status.processing
        db.commit()

        logger.info(
            "processing_started",
            extra={"document_id": document_id},
        )

        file_path = Path("uploads") / document.stored_filename

        logger.info(
            "pdf_extraction_started",
            extra={
                "document_id": document_id,
                "file": str(file_path),
            },
        )

        text = extract_text(str(file_path))

        logger.info(
            "pdf_extraction_completed",
            extra={
                "document_id": document_id,
                "text_length": len(text),
            },
        )

        document.summary = text[:300]

        document.status = Status.completed
        db.commit()

        logger.info(
            "task_completed",
            extra={
                "document_id": document_id,
                "summary_length": len(document.summary or ""),
            },
        )

        return None

    except Exception as e:
        db.rollback()

        logger.exception(
            "task_failed",
            extra={"document_id": document_id, "error": str(e)},
        )

        stmt = select(Document).where(Document.id == document_id)
        document = db.execute(stmt).scalars().first()

        if document:
            document.status = Status.failed
            db.commit()

            logger.error(
                "document_marked_failed",
                extra={"document_id": document_id},
            )

        raise self.retry(exc=e)

    finally:
        release_lock(lock_key)

        logger.info(
            "lock_released",
            extra={"document_id": document_id},
        )

        db.close()