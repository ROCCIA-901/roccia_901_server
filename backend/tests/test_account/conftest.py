from unittest.mock import patch

import pytest

from tests.test_account.factories import UserFactory


@pytest.fixture
def mock_send_mail():
    with patch("account.tasks.send_mail") as mock:
        yield mock


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "Password1!",
        "password_confirmation": "Password1!",
        "username": "홍길동",
        "generation": "11기",
        "role": "부원",
        "workout_location": "더클라임 신림",
        "workout_level": "빨간색",
        "profile_number": 1,
        "introduction": "안녕하세요.",
    }


@pytest.fixture
def mock_cache():
    with patch("django.core.cache.cache.get") as mock:
        yield mock


@pytest.fixture
def mock_exists():
    with patch("django.db.models.query.QuerySet.exists") as mock:
        yield mock


@pytest.fixture
def user_login_data():
    return {
        "email": "test@example.com",
        "password": "Password1!",
    }


@pytest.fixture
def mock_authenticate():
    with patch("account.serializers.authenticate") as mock:
        yield mock


@pytest.fixture
def mock_user_model():
    return UserFactory.build()
