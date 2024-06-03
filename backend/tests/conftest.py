import datetime

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from account.models import User
from record.models import BoulderProblem, Record


@pytest.fixture
def default_user(mock_records):
    instance = baker.make(
        User,
        id=1,
        email="defaultuser@example.com",
        username="defaultuser",
        generation="8기",
        role="운영진",
        workout_location="양재",
        workout_level=4,
        profile_number=1,
        introduction="안녕하세요",
    )
    instance.set_password("Password1!")
    instance.is_active = True
    instance.save()
    return instance


@pytest.fixture
def mock_records(mock_boulder_problem):
    record1 = baker.make(
        Record,
        id=1,
        workout_location="더클라임 연남",
        start_time=datetime.datetime(2024, 5, 5, 10, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        end_time=datetime.datetime(2024, 5, 5, 12, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        user_id=1,
    )

    record2 = baker.make(
        Record,
        id=2,
        workout_location="더클라임 신촌",
        start_time=datetime.datetime(2024, 5, 6, 11, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        end_time=datetime.datetime(2024, 5, 6, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        user_id=1,
    )

    record3 = baker.make(
        Record,
        id=3,
        workout_location="더클라임 홍대",
        start_time=datetime.datetime(2024, 5, 7, 12, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        end_time=datetime.datetime(2024, 5, 7, 14, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        user_id=1,
    )

    return [record1, record2, record3]


@pytest.fixture
def mock_boulder_problem():
    boulder_problem1 = baker.make(BoulderProblem, id=1, workout_level=4, count=6, record_id=1)

    boulder_problem2 = baker.make(BoulderProblem, id=2, workout_level=5, count=5, record_id=2)

    boulder_problem3 = baker.make(BoulderProblem, id=3, workout_level=6, count=4, record_id=3)

    return [boulder_problem1, boulder_problem2, boulder_problem3]


@pytest.fixture
def api_client():
    return APIClient()
