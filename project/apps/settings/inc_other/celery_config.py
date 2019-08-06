import os
from apps.settings.common import env

BROKER_URL = os.environ.get('BROKER_URL', 'redis://redis/14')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis/15')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env('TIME_ZONE', str, 'Europe/Moscow')
CELERYBEAT_SCHEDULE = {}
