import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diploma_app.settings")

import django
django.setup()

from celery import Celery


app = Celery('diploma_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
