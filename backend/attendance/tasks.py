import logging
from datetime import timedelta

from django.utils import timezone

from attendance.models import Attendance
from config.celery import app

logger = logging.getLogger("django")


@app.task(name="reject_pending_attendances")
def reject_pending_attendances():
    current_date = timezone.now().date()

    yesterday = current_date - timedelta(days=1)
    pending_attendances = Attendance.objects.filter(request_processed_status="대기", request_time__date=yesterday)

    pending_attendances.update(request_processed_status="거절")
