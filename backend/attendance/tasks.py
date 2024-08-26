import logging
from datetime import timedelta

from django.utils import timezone

from account.models import Generation
from attendance.models import Attendance
from config.celery import app

logger = logging.getLogger("django")


@app.task(name="reject_pending_attendances")
def reject_pending_attendances():
    """
    처리되지 않은 '대기' 상태의 출석 요청을 거절 처리 하는 테스크입니다.
    """

    current_date = timezone.now().date()
    yesterday = current_date - timedelta(days=1)
    if Generation.objects.filter(start_date__lte=yesterday, end_date__gte=yesterday).exists():
        pending_attendances = Attendance.objects.filter(request_processed_status="대기", request_time__date=yesterday)
        pending_attendances.update(request_processed_status="거절")
