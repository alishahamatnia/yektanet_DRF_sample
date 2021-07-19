import os
from celery import Celery

app = Celery('advertising_management')
app.autodiscover_tasks()
