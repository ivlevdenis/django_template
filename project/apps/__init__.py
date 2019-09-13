from celery import Celery
from django.conf import settings

app = Celery('django')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
