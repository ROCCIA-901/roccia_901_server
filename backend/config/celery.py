import os

from celery import Celery
from celery.schedules import crontab

env = os.getenv("DJANGO_ENV", "dev")
settings_module = "config.settings.prod" if env == "prod" else "config.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("worker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"

app.conf.beat_schedule = {
    "reject-pending-attendances-midnight": {
        "task": "reject_pending_attendances",
        "schedule": crontab(hour=0, minute=6),
    },
}
