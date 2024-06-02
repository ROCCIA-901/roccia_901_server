import pytest
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db
class TestAccountEndpoints:

    def test_user_registration(self, api_client, mock_cache, mock_exists):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        response = api_client.post(
            "/api/accounts/register/",
            data={
                "email": "test@gmail.com",
                "password": "Asdf1234!",
                "password_confirmation": "Asdf1234!",
                "username": "홍길동",
                "generation": "8기",
                "role": "운영진",
                "workout_location": "더클라임 양재",
                "workout_level": "파란색",
                "profile_number": 1,
                "introduction": "안녕하세요",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["detail"] == "회원가입에 성공했습니다. 관리자에게 승인 문의 바랍니다."
        assert "user" in response.data["data"]
        assert response.data["data"]["user"]["email"] == "test@gmail.com"
        assert response.data["data"]["user"]["username"] == "홍길동"

    def test_user_login(self, default_user, api_client):
        response = api_client.post(
            "/api/accounts/login/",
            data={"email": "defaultuser@example.com", "password": "Password1!"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "로그인에 성공했습니다."
        assert "access" in response.data["data"]["token"]
        assert "refresh" in response.data["data"]["token"]

    def test_user_register_auth_code_request(self, api_client, mock_randint, mock_send_mail_task):
        mock_randint.return_value = 12345
        test_email = "testuser@example.com"
        response = api_client.post(
            "/api/accounts/user-register-auth-code-request/",
            data={"email": test_email},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "회원가입을 위한 인증번호가 전송됐습니다."

        assert cache.get(f"{test_email}:register:code") == 12345
        assert cache.get(f"{test_email}:register:status") == "uncertified"

        mock_send_mail_task.assert_called_once_with("회원가입", test_email, 12345)

    def test_user_register_auth_code_verify(self, api_client):
        test_email = "testuser@example.com"
        auth_code = 12345

        cache.set(f"{test_email}:register:code", auth_code)
        cache.set(f"{test_email}:register:status", "uncertified")

        response = api_client.post(
            "/api/accounts/user-register-auth-code-verify/",
            data={"email": test_email, "code": auth_code},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "회원가입을 위한 인증번호 확인에 성공했습니다. 인증은 1시간 동안 유효합니다."

        assert cache.get(f"{test_email}:register:status") == "certified"

    def test_token_refresh(self, api_client, default_user):
        login_response = api_client.post(
            "/api/accounts/login/",
            data={"email": "defaultuser@example.com", "password": "Password1!"},
            format="json",
        )

        assert login_response.status_code == status.HTTP_200_OK
        refresh_token = login_response.data["data"]["token"]["refresh"]

        response = api_client.post(
            "/api/accounts/token-refresh/",
            data={"refresh": refresh_token},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "액세스 토큰 발급을 성공했습니다."
        assert "access" in response.data["data"]["token"]
