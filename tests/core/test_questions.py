from unittest import mock

from beauty_ocean.core import questions


@mock.patch("beauty_ocean.core.api.get_account_data")
@mock.patch("beauty_ocean.core.config.answer")
def test_ask_for_account_confirmation(mock_answer, mock_get_account_data):
    manager = mock.Mock()
    mock_answer.return_value = True
    ans = questions.confirm_account(manager)

    assert mock_get_account_data.call_count == 1
    assert ans
