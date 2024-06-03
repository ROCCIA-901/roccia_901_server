import pytest
from rest_framework import status


@pytest.mark.django_db
class TestMyageEndpoints:

    @pytest.fixture(autouse=True)
    def setup(self, default_user, api_client):
        self.api_client = api_client
        self.default_user = default_user
        login_res = self.api_client.post(
            "/api/accounts/login/",
            data={"email": "defaultuser@example.com", "password": "Password1!"},
            format="json",
        )
        assert login_res.status_code == status.HTTP_200_OK, login_res.data
        self.access_token = login_res.data["data"]["token"]["access"]

    def test_retrieve_mypage_without_user_id(self):
        mypage_res = self.api_client.get(
            "/api/mypages/",
            headers={"Authorization": f"Bearer {self.access_token}"},
            format="json",
        )

        assert mypage_res.status_code == status.HTTP_200_OK
        assert mypage_res.data["detail"] == "마이페이지 조회를 성공했습니다."
        assert "profile" in mypage_res.data["data"]
        assert "total_workout_time" in mypage_res.data["data"]
        assert "records" in mypage_res.data["data"]

    def test_retrieve_mypage_with_user_id(self):
        mypage_res = self.api_client.get(
            "/api/mypages/",
            data={"user_id": self.default_user.id},
            headers={"Authorization": f"Bearer {self.access_token}"},
            format="json",
        )

        assert mypage_res.status_code == status.HTTP_200_OK
        assert mypage_res.data["detail"] == "마이페이지 조회를 성공했습니다."
