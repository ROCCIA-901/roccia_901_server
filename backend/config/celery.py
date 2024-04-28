import os

from celery import Celery

env = os.getenv("DJANGO_ENV", "dev")
settings_module = "config.settings.prod" if env == "prod" else "config.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("worker")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
