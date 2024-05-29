import pytest

from tests.test_account.factories import UserFactory


@pytest.fixture
def mock_user_model():
    return UserFactory.build()
