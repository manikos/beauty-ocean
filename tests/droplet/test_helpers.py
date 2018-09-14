import tempfile
from unittest import mock

import pytest
from digitalocean import SSHKey

from beauty_ocean.droplet import helpers
from tests.conftest import DUMMY_PUBLIC_KEY


def test_validate_public_key():
    with tempfile.NamedTemporaryFile() as f:
        f.write(bytes(DUMMY_PUBLIC_KEY, encoding="utf-8"))
        f.seek(0)
        res = helpers.validate_public_key(f.name)
        assert res == DUMMY_PUBLIC_KEY

    with tempfile.NamedTemporaryFile() as f:
        f.write(b"corrupt-public-key")
        f.seek(0)
        with pytest.raises(Exception):
            helpers.validate_public_key(f.name)


@mock.patch("beauty_ocean.droplet.api.create_ssh_key")
@mock.patch("beauty_ocean.droplet.questions.ask_for_public_key_name")
def test_post_public_key(m_ask_for_public_key_name, m_create_ssh_key):
    name = "public_key_name"
    m_ask_for_public_key_name.return_value = name
    m_create_ssh_key.return_value = SSHKey(name=name)
    res = helpers.post_public_key("token", "public_key")
    assert m_ask_for_public_key_name.call_count == 1
    assert m_create_ssh_key.call_count == 1
    assert type(res) is list
    assert len(res) == 1
    assert type(res[0]) is SSHKey


@mock.patch("beauty_ocean.droplet.helpers.post_public_key")
@mock.patch("beauty_ocean.droplet.helpers.validate_public_key")
@mock.patch("beauty_ocean.droplet.questions.ask_for_public_key_path")
def test_handle_ssh_keys_local(
    m_ask_for_public_key_path, m_validate_public_key, m_post_public_key
):
    m = mock.Mock()
    m_ask_for_public_key_path.return_value = "path/to/public/key"
    m_validate_public_key.return_value = None
    res = helpers.handle_ssh_keys(manager=m, addition_method="local")
    msg = "Enter the path to your public key"
    m_ask_for_public_key_path.assert_called_once_with(msg)
    assert res == []

    m_validate_public_key.return_value = DUMMY_PUBLIC_KEY
    __ = helpers.handle_ssh_keys(manager=m, addition_method="local")
    m_post_public_key.assert_called_once_with(m.token, DUMMY_PUBLIC_KEY)


@mock.patch("beauty_ocean.droplet.helpers.validate_public_key")
@mock.patch("beauty_ocean.droplet.questions.ask_for_public_key_path")
@mock.patch("beauty_ocean.droplet.questions.ask_for_remote_ssh_keys_selection")
def test_handle_ssh_keys_remote(
    m_ask_for_remote_ssh_keys_selection,
    m_ask_for_public_key_path,
    m_validate_public_key,
):
    m = mock.Mock()
    msg = "No ssh keys selected or found on DO! " \
          "Enter the path to your public key"
    m_ask_for_remote_ssh_keys_selection.return_value = []
    m_ask_for_public_key_path.return_value = "path/to/public/key"
    m_validate_public_key.return_value = None
    helpers.handle_ssh_keys(manager=m, addition_method="remote")

    m_ask_for_remote_ssh_keys_selection.assert_called_once_with(m)
    m_ask_for_public_key_path.assert_called_once_with(msg)

    m_ask_for_remote_ssh_keys_selection.return_value = [SSHKey(name='name')]
    res = helpers.handle_ssh_keys(manager=m, addition_method="remote")
    assert type(res) is list
    assert len(res) == 1
    assert type(res[0]) is SSHKey
    assert res[0].name == 'name'


@mock.patch("beauty_ocean.droplet.questions.ask_for_new_tag")
@mock.patch("beauty_ocean.droplet.questions.ask_for_remote_tag_selection")
def test_handle_tag_selection(
    m_ask_for_remote_tag_selection, m_ask_for_new_tag
):
    m = mock.Mock()
    tags = ["remote-tag-1", "remote-tag-2"]

    # empty remote tags
    m_ask_for_remote_tag_selection.return_value = []
    helpers.handle_tag_selection(manager=m, both=False)
    msg = "No remote tags found ¯\_(ツ)_/¯! " \
          "Enter one or more tags (comma and space separated, i.e tag1, tag2)"
    m_ask_for_new_tag.assert_called_once_with(message=msg)

    # non-empty remote tags
    m_ask_for_remote_tag_selection.return_value = tags
    res = helpers.handle_tag_selection(m, both=False)
    assert res == ["remote-tag-1", "remote-tag-2"]

    # both (remote and new ones)
    m_ask_for_new_tag.reset_mock()
    m_ask_for_remote_tag_selection.return_value = tags
    m_ask_for_new_tag.return_value = ["remote-tag-3"]
    res = helpers.handle_tag_selection(m, both=True)
    assert m_ask_for_new_tag.call_count == 1
    assert res == ["remote-tag-1", "remote-tag-2", "remote-tag-3"]


@mock.patch("beauty_ocean.droplet.questions.ask_for_new_tag")
@mock.patch("beauty_ocean.droplet.helpers.handle_tag_selection")
def test_handle_tags(m_handle_tag_selection, m_ask_for_new_tag):
    m = mock.Mock()
    helpers.handle_tags(m, addition_method="remote")
    m_handle_tag_selection.assert_called_once_with(m)

    helpers.handle_tags(m, addition_method="new")
    assert m_ask_for_new_tag.call_count == 1

    m_handle_tag_selection.reset_mock()
    helpers.handle_tags(m, addition_method="both")
    m_handle_tag_selection.assert_called_once_with(m, both=True)


def test_padding_text():
    assert helpers.padding_text("hello", length=11) == "\n---HELLO---\n"
    assert helpers.padding_text("cat", length=7, pad="+") == "\n++CAT++\n"


def test_review_droplet_data(capsys):
    data = {"id": 1, "name": "my_droplet", "token": "fake-token"}
    helpers.review_droplet_data(data=data)
    captured = capsys.readouterr()
    text_1 = "'id': 1"
    text_2 = "'name': 'my_droplet'"
    text_3 = "DROPLET CONFIGURATION"
    text_4 = "END DROPLET CONFIGURATION"
    assert text_1 in captured.out
    assert text_2 in captured.out
    assert text_3 in captured.out
    assert text_4 in captured.out


@mock.patch('beauty_ocean.droplet.api.poll_droplet')
@mock.patch('beauty_ocean.droplet.api.boot_droplet')
def test_create_droplet_now(m_boot_droplet, m_poll_droplet, capsys):
    droplet_params = {
        'image': 'ubuntu-18-04-x64',
        'name': 'digital_ocean',
    }
    helpers.create_droplet_now(droplet_params=droplet_params)
    captured = capsys.readouterr()
    assert m_boot_droplet.call_count == 1
    assert m_poll_droplet.call_count == 1
    assert "Droplet initialized! Booting..." in captured.out
    assert "Droplet has been created successfully! \(´▽`)/" in captured.out


def test_filter_droplet_return_data(dummy_droplet):
    res = helpers.filter_droplet_return_data(dummy_droplet)
    assert type(res) is dict
    assert "token" not in res
    assert "_log" not in res
    assert res["ssh_keys"] == ["ssh1", "ssh2"]


def test_droplet_data_json(dummy_droplet):
    res = helpers.droplet_data_json(dummy_droplet)
    assert type(res) == str
