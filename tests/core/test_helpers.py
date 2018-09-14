import tempfile
from unittest import mock

import pytest
from digitalocean import Manager

from beauty_ocean.core import helpers
from tests.conftest import unset_env


def test_get_token_empty():
    with unset_env("DO_TOKEN"):
        with pytest.raises(ValueError, match=r"^Token not found .*"):
            helpers.get_token()


def test_get_token_invalid():
    with pytest.raises(ValueError, match=r"^Token was not found .*"):
        helpers.get_token("")


def test_get_token():
    dummy_token = "fake-api-token-here"
    with mock.patch.dict('os.environ', {'DO_TOKEN': dummy_token}):
        assert helpers.get_token() == dummy_token

    with mock.patch.dict('os.environ', {'MY_TOKEN': dummy_token}):
        assert helpers.get_token("MY_TOKEN") == dummy_token

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(b"fake")
        fp.seek(0)
        assert helpers.get_token(fp.name) == "fake"

    assert (
        helpers.get_token("some-random-string-here")
        == "some-random-string-here"
    )


@mock.patch("beauty_ocean.core.helpers.get_token")
def test_create_manager(mock_get_token):
    t = "fake-key"
    res = helpers.create_manager(t)
    mock_get_token.assert_called_once_with(t)
    assert type(res) is Manager


def test_read_path():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"public-key-here")
        f.seek(0)
        assert helpers.read_path(f.name) == "public-key-here"
