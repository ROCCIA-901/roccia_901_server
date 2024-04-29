from unittest.mock import patch

import pytest


@pytest.fixture
def mock_send_mail():
    with patch("account.tasks.send_mail") as mock:
        yield mock
