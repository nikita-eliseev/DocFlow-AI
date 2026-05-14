from celery import Celery


celery_app = Celery(
    "docflow",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    task_acks_late=True,             
    worker_prefetch_multiplier=1,   

    task_default_retry_delay=5,
    task_max_retries=3,
)

celery_app.autodiscover_tasks(["worker"])