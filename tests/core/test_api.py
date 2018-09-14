from unittest.mock import Mock

from beauty_ocean.core import api


def test_get_account_data():
    manager = Mock()
    api.get_account_data(manager)
    assert manager.get_account.call_count == 1
