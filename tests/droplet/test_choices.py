from beauty_ocean.droplet import choices


def test_prepare_image_type_choices():
    c = [
        ("Distribution only", "distribution"),
        ("Application only", "application"),
        ("All available images", "all"),
    ]
    assert choices.prepare_image_type_choices() == c


def test_prepare_image_choices(do_images):
    to_equal = [
        ("16.04.04 (Ubuntu)", do_images[0]),
        ("27 x64 (Fedora)", do_images[2]),
        ("8.5 x64 (Debian)", do_images[-2]),
    ]
    assert choices.prepare_image_choices(do_images) == to_equal


def test_prepare_region_choices(do_regions):
    to_equal = [
        ("Amsterdam 1", do_regions[-2]),
        ("Amsterdam 2", do_regions[2]),
        ("Frankfurt 1", do_regions[-1]),
        ("New York 2", do_regions[1]),
        ("Toronto 3", do_regions[0]),
    ]
    assert choices.prepare_region_choices(do_regions) == to_equal


def test_prepare_size_choices(do_sizes):
    to_equal = [
        (
            f"{'s-1vcpu-1gb':15} | {'€5.0/mo':10} | {'CPUs: 1':^10}",
            do_sizes[2],
        ),
        (
            f"{'s-1vcpu-2gb':15} | {'€10.0/mo':10} | {'CPUs: 1':^10}",
            do_sizes[0],
        ),
        (f"{'1gb':15} | {'€10.0/mo':10} | {'CPUs: 1':^10}", do_sizes[-1]),
        (
            f"{'s-1vcpu-3gb':15} | {'€15.0/mo':10} | {'CPUs: 2':^10}",
            do_sizes[-2],
        ),
        (
            f"{'s-2vcpu-2gb':15} | {'€20.0/mo':10} | {'CPUs: 2':^10}",
            do_sizes[1],
        ),
    ]
    assert choices.prepare_size_choices(do_sizes) == to_equal


def test_prepare_ssh_keys_addition_method_choices():
    to_equal = [
        (
            "Load ssh keys from your DO account "
            "(you'll be asked which one(s) to use on next step)",
            "remote",
        ),
        ("Load ssh public key from your local filesystem", "local"),
    ]
    assert choices.prepare_ssh_keys_addition_method_choices() == to_equal


def test_prepare_ssh_key_choices(do_ssh):
    to_equal = [
        (
            "fake_key_1: 44:90:8c:62:6e:53:3b:d8:1a:67:34:2f:94:02:e4:87",
            do_ssh[0],
        ),
        (
            "fake_key_2: 66:a1:2a:23:4d:5c:8b:58:e7:ef:2f:e5:49:3b:3d:32",
            do_ssh[1],
        ),
        (
            "fake_key_3: aa:bb:cc:dd:ee:ff:aa:bb:cc:dd:ee:ff:aa:bb:cc:dd",
            do_ssh[2],
        ),
    ]
    assert choices.prepare_ssh_key_choices(do_ssh) == to_equal


def test_prepare_tag_addition_method_choices():
    to_equal = [
        ("Add remote (existing) tags only", "remote"),
        ("Add new tags only", "new"),
        ("Both remote and new tags", "both"),
    ]
    assert choices.prepare_tag_addition_method_choices() == to_equal


def test_prepare_tag_choices(do_tags):
    to_equal = [
        ("tag1", do_tags[0]),
        ("tag2", do_tags[1]),
        ("tag3", do_tags[2]),
    ]
    assert choices.prepare_remote_tag_choices(do_tags) == to_equal
