from unittest.mock import patch

import pytest

from tests.test_account.factories import UserFactory


@pytest.fixture
def mock_user_model():
    return UserFactory.build()


@pytest.fixture
def mock_boulder_problem_object():
    with patch("record.models.BoulderProblem.objects.filter") as mock:
        yield mock


@pytest.fixture
def mock_record_object():
    with patch("record.models.Record.objects.filter") as mock:
        yield mock
