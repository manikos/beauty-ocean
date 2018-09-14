from unittest import mock

from beauty_ocean.droplet import questions


def test_questions_constants():
    assert (
        questions.NEW_TAG_MSG
        == "Enter one or more tags (comma and space separated, i.e tag1, tag2)"
    )


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_image_type(m_answer):
    m_answer.return_value = "an_image_type"
    ans = questions.ask_for_image_type()

    assert m_answer.call_count == 1
    assert ans == "an_image_type"


@mock.patch("beauty_ocean.droplet.api.get_all_images")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_image(m_answer, m_get_all_images, do_images):
    manager = mock.Mock()
    m_get_all_images.return_value = do_images
    m_answer.return_value = do_images[0]
    image, regions = questions.ask_for_image(
        manager=manager, image_type="distribution"
    )

    m_get_all_images.assert_called_once_with(manager, "distribution")
    assert m_answer.call_count == 1
    assert image == do_images[0]
    assert regions == ["reg1", "reg2", "reg3"]


@mock.patch("beauty_ocean.droplet.api.get_all_regions")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_region(m_answer, m_get_all_regions, do_regions):
    manager = mock.Mock()
    m_get_all_regions.return_value = do_regions
    m_answer.return_value = do_regions[0]
    region, sizes = questions.ask_for_region(
        manager=manager, available_regions=do_regions
    )

    m_get_all_regions.assert_called_once_with(manager)
    assert m_answer.call_count == 1
    assert region == do_regions[0]
    assert sizes == ["siz1", "siz2", "siz3"]


@mock.patch("beauty_ocean.droplet.api.get_all_sizes")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_size(m_answer, m_get_all_sizes, do_sizes):
    manager = mock.Mock()
    m_get_all_sizes.return_value = do_sizes
    m_answer.return_value = do_sizes[0]
    size = questions.ask_for_size(manager=manager, available_sizes=do_sizes)

    m_get_all_sizes.assert_called_once_with(manager)
    assert m_answer.call_count == 1
    assert size == do_sizes[0]


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_droplet_name(m_answer):
    m_answer.return_value = "droplet_name"
    name = questions.ask_for_droplet_name()
    assert m_answer.call_count == 1
    assert name == "droplet_name"


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_confirm_ssh_addition(m_answer):
    m_answer.return_value = True
    confirm = questions.confirm_ssh_addition()
    assert m_answer.call_count == 1
    assert confirm


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_ssh_keys_addition_method(m_answer):
    m_answer.return_value = "remote"
    method = questions.ask_for_ssh_keys_addition_method()
    assert m_answer.call_count == 1
    assert method == "remote"


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_confirm_backups_addition(m_answer):
    m_answer.return_value = False
    confirm = questions.confirm_backups_addition()
    assert m_answer.call_count == 1
    assert not confirm


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_confirm_ipv6_addition(m_answer):
    m_answer.return_value = False
    confirm = questions.confirm_ipv6_addition()
    assert m_answer.call_count == 1
    assert not confirm


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_confirm_tags_addition(m_answer):
    m_answer.return_value = False
    confirm = questions.confirm_tags_addition()
    assert m_answer.call_count == 1
    assert not confirm


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_tag_addition_method(m_answer):
    m_answer.return_value = "both"
    method = questions.ask_for_tag_addition_method()
    assert m_answer.call_count == 1
    assert method == "both"


@mock.patch("beauty_ocean.droplet.questions.tag_answer")
def test_ask_for_new_tag(m_tag_answer):
    m_tag_answer.return_value = "both"
    method = questions.ask_for_new_tag()
    assert m_tag_answer.call_count == 1
    assert method == "both"


@mock.patch("beauty_ocean.droplet.api.get_remote_ssh_keys")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_remote_ssh_keys_selection(
    m_answer, m_get_remote_ssh_keys, do_ssh
):
    manager = mock.Mock()
    m_get_remote_ssh_keys.return_value = do_ssh
    m_answer.return_value = [do_ssh[0]]
    ssh_keys = questions.ask_for_remote_ssh_keys_selection(manager=manager)

    m_get_remote_ssh_keys.assert_called_once_with(manager)
    assert m_answer.call_count == 1
    assert type(ssh_keys) is list
    assert ssh_keys == [do_ssh[0]]

    m_answer.reset_mock()
    m_get_remote_ssh_keys.return_value = []
    ssh_keys = questions.ask_for_remote_ssh_keys_selection(manager=manager)
    assert not m_answer.called
    assert ssh_keys == []


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_public_key_path(m_answer):
    m_answer.return_value = "path/to/public/key"
    path = questions.ask_for_public_key_path("the question here")
    assert m_answer.call_count == 1
    assert path == "path/to/public/key"


@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_public_key_name(m_answer):
    m_answer.return_value = "public_key_name"
    name = questions.ask_for_public_key_name()
    assert m_answer.call_count == 1
    assert name == "public_key_name"


@mock.patch("beauty_ocean.droplet.api.get_remote_tags")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_ask_for_remote_tag_selection(
    m_answer, m_get_remote_tags, do_tags
):
    manager = mock.Mock()
    m_get_remote_tags.return_value = do_tags
    m_answer.return_value = [do_tags[0]]
    tags = questions.ask_for_remote_tag_selection(manager=manager)

    m_get_remote_tags.assert_called_once_with(manager)
    assert m_answer.call_count == 1
    assert type(tags) is list
    assert tags == [do_tags[0]]

    m_answer.reset_mock()
    m_get_remote_tags.return_value = []
    tags = questions.ask_for_remote_tag_selection(manager=manager)
    assert not m_answer.called
    assert tags == []


@mock.patch("beauty_ocean.droplet.helpers.review_droplet_data")
@mock.patch("beauty_ocean.droplet.questions.answer")
def test_confirm_droplet_data(m_answer, m_review_droplet_data):
    droplet_params = {"image": "ubuntu-18-04-x64", "name": "digital_ocean"}
    m_answer.return_value = True
    confirm = questions.confirm_droplet_data(droplet_params=droplet_params)
    m_review_droplet_data.assert_called_once_with(droplet_params)
    assert m_answer.call_count == 1
    assert confirm
