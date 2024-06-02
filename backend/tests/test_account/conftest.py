from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.cache import cache
from model_bakery import baker
from rest_framework.test import APIClient

from account.models import User
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
def mock_active_user_filter_queryset():
    with patch("account.models.User.objects.filter") as mock:
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


@pytest.fixture
def mock_token_refresh_serializer_validate(mock_user_model):
    with patch("rest_framework_simplejwt.serializers.TokenRefreshSerializer.validate") as mock:
        yield mock


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def default_user():
    instance = baker.make(User, id=1, email="defaultuser@example.com", username="defaultuser")
    instance.set_password("Password1!")
    instance.is_active = True
    instance.save()
    return instance


@pytest.fixture
def mock_randint():
    with patch("random.randint") as mock:
        yield mock


@pytest.fixture(scope="session", autouse=True)
def configure_settings():
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    cache.clear()


@pytest.fixture
def mock_send_mail_task():
    with patch("account.tasks.send_auth_code_to_email.delay") as mock:
        yield mock
