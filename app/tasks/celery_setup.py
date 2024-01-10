from celery import Celery

from app.config import settings

celery_worker = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=[
        'app.tasks.tasks',
        'app.tasks.scheduled',
        ]
)
