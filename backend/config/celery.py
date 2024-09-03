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
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    "reject_pending_attendances": {
        "task": "reject_pending_attendances",
        "schedule": crontab(hour=23, minute=57),
    },
    "holiday_processing": {
        "task": "holiday_processing",
        "schedule": crontab(hour=23, minute=58),
    },
    "absence_processing": {
        "task": "absence_processing",
        "schedule": crontab(hour=23, minute=59),
    },
}
