import logging

from django.core.mail import send_mail

from config.celery import app

logger = logging.getLogger("django")


@app.task(name="worker")
def send_auth_code_to_email(type: str, receiver: str, code: int) -> None:
    try:
        email_subject = "[ROCCIA 901] 본인 확인 인증 번호 입니다."
        email_body = f"{type}을 위해 전송된 이메일입니다.\n 본인확인을 위해 인증 번호 [{code}]를 입력해 주세요."

        send_mail(subject=email_subject, message=email_body, from_email="ROCCIA 901", recipient_list=[receiver])
    except Exception as e:
        logger.error(f"{type} 인증 이메일 전송 실패 - {receiver}, 에러: {str(e)}")
