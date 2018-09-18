from unittest import mock

import pytest
from digitalocean import Image, Region, Size

from beauty_ocean.droplet.entry import create_droplet


@mock.patch("beauty_ocean.core.questions.confirm_account")
@mock.patch("beauty_ocean.core.helpers.create_manager")
def test_create_droplet_decline_account(
    m_create_manager, m_confirm_account, capsys
):
    manager = mock.Mock()
    err = "Please run the script with the preferred API token. " \
          "Thanks for using this tool! ♥"
    m_create_manager.return_value = manager
    m_confirm_account.return_value = False
    with pytest.raises(SystemExit) as sys_call:
        res = create_droplet("token")
        captured = capsys.readouterr()
        assert res is None
        assert err in captured.out
    m_create_manager.assert_called_once_with("token")
    assert sys_call.type == SystemExit
    assert sys_call.value.code == 0


@mock.patch("beauty_ocean.droplet.entry.questions")
@mock.patch("beauty_ocean.core.questions.confirm_account")
@mock.patch("beauty_ocean.core.helpers.create_manager")
def test_create_droplet_decline_droplet_data(
    m_create_manager, m_confirm_account, m_questions, capsys
):
    manager = mock.Mock()
    m_create_manager.return_value = manager
    m_confirm_account.return_value = True
    m_questions.ask_for_image_type.return_value = "all"
    m_questions.ask_for_image.return_value = (
        Image(name="ubuntu 18", slug="ubuntu-18"),
        ["ams1", "nyc1", "ams2"],
    )
    m_questions.ask_for_region.return_value = (
        Region(name="Amsterdam 1", slug="ams-1"),
        ["1gb", "2gb", "5gb"],
    )
    m_questions.ask_for_size.return_value = Size(name="1 GB", slug="1gb")
    m_questions.ask_for_droplet_name.return_value = "droplet_name"
    m_questions.confirm_ssh_addition.return_value = False
    m_questions.confirm_backups_addition.return_value = False
    m_questions.confirm_ipv6_addition.return_value = False
    m_questions.confirm_tags_addition.return_value = False
    m_questions.confirm_droplet_data.return_value = False
    res = create_droplet("token")
    captured = capsys.readouterr()
    assert "Configuration declined!" in captured.out
    assert res is None


@mock.patch("beauty_ocean.droplet.entry.helpers")
@mock.patch("beauty_ocean.droplet.entry.questions")
@mock.patch("beauty_ocean.core.questions.confirm_account")
@mock.patch("beauty_ocean.core.helpers.create_manager")
def test_create_droplet_scenario_1(
    m_create_manager, m_confirm_account, m_questions, m_helpers
):
    manager = mock.Mock()
    m_create_manager.return_value = manager
    m_confirm_account.return_value = True
    m_questions.ask_for_image_type.return_value = "all"
    m_questions.ask_for_image.return_value = (
        Image(name="ubuntu 18", slug="ubuntu-18"),
        ["ams1", "nyc1", "ams2"],
    )
    m_questions.ask_for_region.return_value = (
        Region(name="Amsterdam 1", slug="ams-1"),
        ["1gb", "2gb", "5gb"],
    )
    m_questions.ask_for_size.return_value = Size(name="1 GB", slug="1gb")
    m_questions.ask_for_droplet_name.return_value = "droplet_name"
    m_questions.confirm_ssh_addition.return_value = False
    m_questions.confirm_backups_addition.return_value = False
    m_questions.confirm_ipv6_addition.return_value = False
    m_questions.confirm_tags_addition.return_value = False
    m_questions.confirm_droplet_data.return_value = True

    droplet_params = {
        "token": manager.token,
        "name": "droplet_name",
        "size_slug": "1gb",
        "image": "ubuntu-18",
        "region": "ams-1",
        "ssh_keys": [],
        "backups": False,
        "ipv6": False,
        "tags": [],
    }
    create_droplet("token")
    assert m_helpers.droplet_data_json.call_count == 1
    m_helpers.create_droplet_now.assert_called_once_with(droplet_params)


@mock.patch("beauty_ocean.droplet.entry.helpers")
@mock.patch("beauty_ocean.droplet.entry.questions")
@mock.patch("beauty_ocean.core.questions.confirm_account")
@mock.patch("beauty_ocean.core.helpers.create_manager")
def test_create_droplet_scenario_2(
    m_create_manager, m_confirm_account, m_questions, m_helpers
):
    manager = mock.Mock()
    m_create_manager.return_value = manager
    m_confirm_account.return_value = True
    m_questions.ask_for_image_type.return_value = "all"
    m_questions.ask_for_image.return_value = (
        Image(name="ubuntu 18", slug="ubuntu-18"),
        ["ams1", "nyc1", "ams2"],
    )
    m_questions.ask_for_region.return_value = (
        Region(name="Amsterdam 1", slug="ams-1"),
        ["1gb", "2gb", "5gb"],
    )
    m_questions.ask_for_size.return_value = Size(name="1 GB", slug="1gb")
    m_questions.ask_for_droplet_name.return_value = "droplet_name"
    m_questions.confirm_ssh_addition.return_value = True
    m_questions.ask_for_ssh_keys_addition_method.return_value = "local"
    m_helpers.handle_ssh_keys.return_value = ["ssh_fingerprint1"]
    m_questions.confirm_backups_addition.return_value = False
    m_questions.confirm_ipv6_addition.return_value = False
    m_questions.confirm_tags_addition.return_value = False
    m_questions.confirm_droplet_data.return_value = True

    droplet_params = {
        "token": manager.token,
        "name": "droplet_name",
        "size_slug": "1gb",
        "image": "ubuntu-18",
        "region": "ams-1",
        "ssh_keys": ["ssh_fingerprint1"],
        "backups": False,
        "ipv6": False,
        "tags": [],
    }
    create_droplet("token")
    m_helpers.handle_ssh_keys.assert_called_once_with(manager, "local")
    m_helpers.create_droplet_now.assert_called_once_with(droplet_params)
    assert m_helpers.droplet_data_json.call_count == 1


@mock.patch("beauty_ocean.droplet.entry.helpers")
@mock.patch("beauty_ocean.droplet.entry.questions")
@mock.patch("beauty_ocean.core.questions.confirm_account")
@mock.patch("beauty_ocean.core.helpers.create_manager")
def test_create_droplet_scenario_3(
    m_create_manager, m_confirm_account, m_questions, m_helpers
):
    manager = mock.Mock()
    m_create_manager.return_value = manager
    m_confirm_account.return_value = True
    m_questions.ask_for_image_type.return_value = "all"
    m_questions.ask_for_image.return_value = (
        Image(name="ubuntu 18", slug="ubuntu-18"),
        ["ams1", "nyc1", "ams2"],
    )
    m_questions.ask_for_region.return_value = (
        Region(name="Amsterdam 1", slug="ams-1"),
        ["1gb", "2gb", "5gb"],
    )
    m_questions.ask_for_size.return_value = Size(name="1 GB", slug="1gb")
    m_questions.ask_for_droplet_name.return_value = "droplet_name"
    m_questions.confirm_ssh_addition.return_value = True
    m_questions.ask_for_ssh_keys_addition_method.return_value = "local"
    m_helpers.handle_ssh_keys.return_value = ["ssh_fingerprint1"]
    m_questions.confirm_backups_addition.return_value = False
    m_questions.confirm_ipv6_addition.return_value = False
    m_questions.confirm_tags_addition.return_value = True
    m_questions.ask_for_tag_addition_method.return_value = "remote"
    m_helpers.handle_tags.return_value = ["tag1", "tag2"]
    m_questions.confirm_droplet_data.return_value = True

    droplet_params = {
        "token": manager.token,
        "name": "droplet_name",
        "size_slug": "1gb",
        "image": "ubuntu-18",
        "region": "ams-1",
        "ssh_keys": ["ssh_fingerprint1"],
        "backups": False,
        "ipv6": False,
        "tags": ["tag1", "tag2"],
    }
    create_droplet("token")
    m_helpers.handle_tags.assert_called_once_with(manager, "remote")
    m_helpers.create_droplet_now.assert_called_once_with(droplet_params)
    assert m_helpers.droplet_data_json.call_count == 1
