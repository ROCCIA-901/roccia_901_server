import pytest

from account.tasks import send_auth_code_to_email

pytestmark = pytest.mark.unit


class TestCeleryWorker:
    def test_send_auth_code_to_email(self, mock_send_mail):
        email_type = "회원가입"
        receiver_email = "test@example.com"
        auth_code = 12345

        send_auth_code_to_email(email_type, receiver_email, auth_code)

        mock_send_mail.assert_called_once_with(
            subject="[ROCCIA 901] 본인 확인 인증 번호 입니다.",
            message=f"{email_type}을 위해 전송된 이메일입니다.\n 본인확인을 위해 인증 번호 [{auth_code}]를 입력해 주세요.",
            from_email="ROCCIA 901",
            recipient_list=[receiver_email],
        )
