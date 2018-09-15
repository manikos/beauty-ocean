import re
from typing import Tuple, List

from digitalocean import Manager, Image, Region

from beauty_ocean.core.config import (
    answer,
    tag_answer,
    question,
    q_radio,
    q_confirm,
    q_multiple,
)
from beauty_ocean.droplet import api, choices, helpers


NEW_TAG_MSG = (
    "Enter one or more tags (comma and space separated, i.e tag1, tag2)"
)


def ask_for_image_type() -> str:
    """
    Prompts the user to select an image type (distribution, application, all).

    :return: str (the selected image type)
    """
    q = q_radio(
        message="Select an image type",
        choices=choices.prepare_image_type_choices(),
    )
    selected_image_type = answer(q)
    return selected_image_type


def ask_for_image(manager: Manager, image_type: str) -> Tuple[Image, list]:
    """
    Given an image type, prompts the user to select one of the available images
    (Ubuntu, Fedora, Debian etc).

    :param Manager manager: instance
    :param str image_type: an image type
    :return: tuple of digitalocean.Image instance and list of Region instances
    """
    # User's image selection
    images = api.get_all_images(manager, image_type)
    q = q_radio(
        message="Select an image",
        choices=choices.prepare_image_choices(images),
    )
    selected_image = answer(q)

    # Get available regions from the selected image
    image_iter = filter(lambda x: x.slug == selected_image.slug, images)
    available_regions = list(image_iter)[0].regions

    return selected_image, available_regions


def ask_for_region(
    manager: Manager, available_regions: list
) -> Tuple[Region, list]:
    """
    Prompts the user to select a region (London, Amsterdam etc).

    :param Manager manager: instance
    :param list available_regions: list of digitalocean.Region instances
    :return: tuple of digitalocean.Region instance and list of Size instances
    """
    # User's region selection
    regions = api.get_all_regions(manager)
    available_regions = list(
        filter(lambda r: r.slug in available_regions and r.available, regions)
    )
    q = q_radio(
        message="Select a region",
        choices=choices.prepare_region_choices(available_regions),
    )
    selected_region = answer(q)

    # Get available sizes from the selected region
    region_iter = filter(lambda x: x.slug == selected_region.slug, regions)
    available_sizes = list(region_iter)[0].sizes

    return selected_region, available_sizes


def ask_for_size(manager: Manager, available_sizes: list):
    """
    Prompts the user to select a droplet size (€5, €10, €15 per month etc).

    :param Manager manager: instance
    :param list available_sizes: list of digitalocean.Size instances
    :return: digitalocean.Size instance
    """
    sizes = api.get_all_sizes(manager)
    available_sizes = list(
        filter(lambda s: s.slug in available_sizes and s.available, sizes)
    )
    q = q_radio(
        message="Select a size",
        choices=choices.prepare_size_choices(available_sizes),
    )
    selected_size = answer(q)
    return selected_size


def ask_for_droplet_name() -> str:
    """
    Present a prompt for the user to enter a name for the droplet.
    Valid droplet name characters: a-z, A-Z, 0-9, . and -

    :return: str (the preferred name)
    """
    pattern = re.compile("^[a-zA-Z0-9]+[-.a-zA-Z0-9]*$")
    q = question(
        message="Enter a name for the droplet",
        validate=lambda _, x: pattern.match(x),
    )
    selected_droplet_name = answer(q)
    return selected_droplet_name


def confirm_ssh_addition() -> bool:
    """
    Choice to add or not ssh keys.

    :return: boolean
    """
    msg = "Add ssh keys\n(if not an email will be sent with the root password)"
    q = q_confirm(message=msg, default=True)
    add_ssh_keys = answer(q)
    return add_ssh_keys


def ask_for_ssh_keys_addition_method() -> str:
    """
    Given some options for addition methods of the ssh keys,
    present a prompt for the user to select one.

    :return: str (the selected addition method)
    """
    ssh_method_choices = choices.prepare_ssh_keys_addition_method_choices()
    q = q_radio(
        message="SSH addition method", choices=ssh_method_choices
    )
    addition_method = answer(q)
    return addition_method


def confirm_backups_addition() -> bool:
    """
    Choice to enable Droplet Backup or not.

    :return: boolean
    """
    q = q_confirm(message="Enable Backups", default=True)
    backup = answer(q)
    return backup


def confirm_ipv6_addition() -> bool:
    """
    Choice for IPv6 support or not.

    :return: boolean
    """
    q = q_confirm(message="Enable IPv6", default=False)
    ipv6 = answer(q)
    return ipv6


def confirm_tags_addition() -> bool:
    """
    Choice to add or not tags.

    :return: boolean
    """
    q = q_confirm(message="Add tags", default=True)
    add_tags = answer(q)
    return add_tags


def ask_for_tag_addition_method() -> str:
    """
    Prompts the user to select an addition method to add tags.

    :return: str (the selected addition method)
    """
    tag_method_choices = choices.prepare_tag_addition_method_choices()
    q = q_radio(
        message="Select a method to add tags", choices=tag_method_choices
    )
    addition_method = answer(q)
    return addition_method


def ask_for_new_tag(message: str = NEW_TAG_MSG) -> List[str]:
    """
    Prompts the user to enter some tag names.

    :param str message: the question message
    :return: list of strings
    """
    pattern = re.compile("^[\da-zA-Z]+[-:\w]*(, [\da-zA-Z]+[-:\w]*)*$")
    q = question(message=message, validate=lambda _, x: pattern.match(x))
    return tag_answer(q)


def ask_for_remote_ssh_keys_selection(manager: Manager) -> list:
    """
    Prompts the user to select one or more remote ssh keys.

    :param Manager manager: instance
    :return: list (one or more ssh key(s))
    """
    ssh_key_list = api.get_remote_ssh_keys(manager)
    if ssh_key_list:
        ssh_key_choices = choices.prepare_ssh_key_choices(ssh_key_list)
        q = q_multiple(
            message="Select one or more ssh keys", choices=ssh_key_choices
        )
        return answer(q)
    return []


def ask_for_public_key_path(message) -> str:
    """
    Prompts the user to enter the path for the public key.

    :param str message: the actual question message string
    :return: str (path to public key)
    """
    q = question(message=message)
    path = answer(q)
    return path


def ask_for_public_key_name() -> str:
    """
    Prompts the user to enter a name for the public key.

    :return: str (name of public key)
    """
    pattern = re.compile("^[a-zA-Z]+[-\w_]*$")
    msg = "Enter a name for this public key (it will be shown next to the " \
          "ssh key in your Digital Ocean account)"
    q = question(message=msg, validate=lambda _, x: pattern.match(x))
    name = answer(q)
    return name


def ask_for_remote_tag_selection(manager) -> list:
    """
    Prompts the user to select one or more remote tags.

    :param Manager manager: instance
    :return: list of strings (the selected tag(s))
    """
    tag_list = api.get_remote_tags(manager)
    if tag_list:
        tag_choices = choices.prepare_remote_tag_choices(tag_list)
        q_remote = q_multiple(
            message="Select one or more tags", choices=tag_choices
        )
        ans = answer(q_remote, func=lambda tags: [tag.name for tag in tags])
        return ans
    return []


def confirm_droplet_data(droplet_params) -> bool:
    """
    Choice to confirm the droplet selected data.

    :param dict droplet_params: dict of selected options for droplet creation
    :return: boolean
    """
    helpers.review_droplet_data(droplet_params)
    msg = "One step before droplet creation!\nConfirm selections"
    q = q_confirm(message=msg, default=True)
    confirm = answer(q)
    return confirm
