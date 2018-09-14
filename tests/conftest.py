import os
import contextlib

import pytest
from digitalocean import Droplet, Image, Region, Size, SSHKey, Tag


@pytest.fixture
def do_images():
    return [
        Image(
            name="16.04.04",
            distribution="Ubuntu",
            type="snapshot",
            public=True,
            slug="ubuntu-16.04.04",
            regions=["reg1", "reg2", "reg3"],
        ),
        Image(
            name="18.04 x64",
            distribution="Ubuntu",
            type="snapshot",
            public=False,
            slug="ubuntu-18.04-x64",
            regions=["reg1", "reg2", "reg5", "reg6"],
        ),
        Image(
            name="27 x64",
            distribution="Fedora",
            type="snapshot",
            public=True,
            slug="fedora-27-x64",
            regions=["reg4", "reg5", "reg6"],
        ),
        Image(
            name="8.5 x64",
            distribution="Debian",
            type="snapshot",
            public=True,
            slug="debian-8.5-x64",
            regions=["reg1", "reg3", "reg5"],
        ),
        Image(
            name="9.5 x64",
            distribution="Debian",
            type="other",
            public=True,
            slug="debian-9.5-x64",
            regions=["reg2", "reg4", "reg6"],
        ),
    ]


@pytest.fixture
def do_regions():
    return [
        Region(
            name="Toronto 3",
            slug="tor3",
            sizes=["siz1", "siz2", "siz3"],
            available=True,
        ),
        Region(
            name="New York 2",
            slug="nyc2",
            sizes=["siz3", "siz5", "siz6"],
            available=False,
        ),
        Region(
            name="Amsterdam 2",
            slug="ams2",
            sizes=["siz4", "siz8"],
            available=True,
        ),
        Region(
            name="Amsterdam 1",
            slug="ams1",
            sizes=["siz1", "siz2"],
            available=True,
        ),
        Region(
            name="Frankfurt 1",
            slug="fra1",
            sizes=["siz1", "siz3"],
            available=True,
        ),
    ]


@pytest.fixture
def do_sizes():
    return [
        Size(slug="s-1vcpu-2gb", price_monthly=10.0, vcpus=1, available=True),
        Size(slug="s-2vcpu-2gb", price_monthly=20.0, vcpus=2, available=True),
        Size(slug="s-1vcpu-1gb", price_monthly=5.0, vcpus=1, available=True),
        Size(slug="s-1vcpu-3gb", price_monthly=15.0, vcpus=2, available=True),
        Size(slug="1gb", price_monthly=10.0, vcpus=1, available=False),
    ]


@pytest.fixture
def do_ssh():
    return [
        SSHKey(
            name="fake_key_1",
            fingerprint="44:90:8c:62:6e:53:3b:d8:1a:67:34:2f:94:02:e4:87",
        ),
        SSHKey(
            name="fake_key_2",
            fingerprint="66:a1:2a:23:4d:5c:8b:58:e7:ef:2f:e5:49:3b:3d:32",
        ),
        SSHKey(
            name="fake_key_3",
            fingerprint="aa:bb:cc:dd:ee:ff:aa:bb:cc:dd:ee:ff:aa:bb:cc:dd",
        ),
    ]


@pytest.fixture
def do_tags():
    return [Tag(name="tag1"), Tag(name="tag2"), Tag(name="tag3")]


@pytest.fixture
def dummy_droplet():
    return Droplet(
        name="d_name",
        _log="a log here",
        token="token-here",
        id=1,
        ssh_keys=[SSHKey(id=1, name="ssh1"), SSHKey(id=1, name="ssh2")],
    )


@contextlib.contextmanager
def unset_env(name):
    env_var = os.environ.pop(name, None)
    if env_var is not None:
        yield
        os.environ[name] = env_var
    else:
        yield


DUMMY_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCV19HvHtuLleL4rWS1" \
                   "WpetgWLJ0" "5FsNK2Qfjq+wAJWCcFqGijlRPmilT5RGh2+/llwy7zAv" \
                   "Xk1kX2jApD8hVZL/4MieN" "E83d9uvLa0oKzMzk4YWu4CigYBvq5IOu" \
                   "wMxwy9H8o1A/Brg41PfGhg++uR9JtsPqnhdGOZi6YvCbmCGSjCWsNVks" \
                   "H0DiQ86CuOYKYMHzjTMbRSB1xWzX8Xjn0BmHe0UAblcWncWDyoF45w7X" \
                   "C7iyypgCjW1zGDcRy6UnsLjh3eXLUAeb5EBs/SWEnYEm/VZa6jD7t3/6" \
                   "n3qyUF/gZMF8xypaS3WEoHRkMzmE8zDJGPWfYIpx51Z8hfcjaf"
