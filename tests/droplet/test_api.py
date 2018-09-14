from unittest.mock import Mock

from beauty_ocean.droplet import api


def test_get_all_images():
    manager = Mock()
    api.get_all_images(manager, image_type="all", text="Hello")
    manager.get_images.assert_called_once_with(type=None)
    manager.reset_mock()
    api.get_all_images(manager, image_type="application", text="Hello")
    manager.get_images.assert_called_once_with(type="application")
    manager.reset_mock()
    api.get_all_images(manager, text="Hello")
    manager.get_images.assert_called_once_with(type="distribution")


def test_get_all_regions():
    manager = Mock()
    api.get_all_regions(manager)
    assert manager.get_all_regions.call_count == 1


def test_get_all_sizes():
    manager = Mock()
    api.get_all_sizes(manager)
    assert manager.get_all_sizes.call_count == 1


def test_get_remote_ssh_keys():
    manager = Mock()
    api.get_remote_ssh_keys(manager)
    assert manager.get_all_sshkeys.call_count == 1


def test_get_remote_tags():
    manager = Mock()
    api.get_remote_tags(manager)
    assert manager.get_all_tags.call_count == 1


def test_create_ssh_key():
    ssh = Mock()
    api.create_ssh_key(ssh)
    assert ssh.create.call_count == 1


def test_boot_droplet():
    droplet = Mock()
    api.boot_droplet(droplet)
    assert droplet.create.call_count == 1


def test_poll_droplet():
    droplet = Mock()
    droplet.action_ids = [1, 2]
    api.poll_droplet(droplet)
    assert droplet.get_action.call_count == 1
    assert droplet.load.call_count == 1
