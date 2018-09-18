#!/usr/bin/env python

import sys

from beauty_ocean.core import helpers as core_helpers
from beauty_ocean.core import questions as core_questions
from beauty_ocean.core.config import p_text
from beauty_ocean.droplet import questions
from beauty_ocean.droplet import helpers


def create_droplet(token: str = None):
    """
    Interactive console questions for Digital Ocean droplet creation.

    :param str token: the DigitalOcean API token
    :return: json (with droplet info)
    """
    # Get user-provided digital ocean API token
    manager = core_helpers.create_manager(token)

    # Ask to continue with this account (for handling multiple DO accounts)
    cont = core_questions.confirm_account(manager)
    if not cont:
        print(
            p_text("Please run the script with the preferred API token. "
                   "Thanks for using this tool! ♥")
        )
        sys.exit(0)

    # Ask for Image Type (distribution, application or all)
    selected_image_type = questions.ask_for_image_type()

    # Ask for Image (Ubuntu, Fedora, Debian etc)
    selected_image, available_regions = questions.ask_for_image(
        manager, selected_image_type
    )

    # Ask for Region (London, Amsterdam etc)
    selected_region, available_sizes = questions.ask_for_region(
        manager, available_regions
    )

    # Ask for Size (€5, €10, €15 per month etc)
    selected_size = questions.ask_for_size(manager, available_sizes)

    # Ask for Droplet Name
    selected_droplet_name = questions.ask_for_droplet_name()

    # Query for ssh keys
    add_ssh_keys = questions.confirm_ssh_addition()
    selected_ssh_key_list = []
    if add_ssh_keys:
        add_method = questions.ask_for_ssh_keys_addition_method()
        selected_ssh_key_list = helpers.handle_ssh_keys(manager, add_method)

    # Ask for Backups
    selected_backup_option = questions.confirm_backups_addition()

    # Ask for IPv6
    selected_ipv6_option = questions.confirm_ipv6_addition()

    # Ask for Tag(s)
    add_tags = questions.confirm_tags_addition()
    selected_tags = []
    if add_tags:
        add_method = questions.ask_for_tag_addition_method()
        selected_tags = helpers.handle_tags(manager, add_method)

    droplet_params = {
        "token": manager.token,
        "name": selected_droplet_name,
        "size_slug": selected_size.slug,
        "image": selected_image.slug,
        "region": selected_region.slug,
        "ssh_keys": selected_ssh_key_list,
        "backups": selected_backup_option,
        "ipv6": selected_ipv6_option,
        "tags": selected_tags,
    }

    # Review selections
    confirm = questions.confirm_droplet_data(droplet_params)

    if confirm:
        droplet = helpers.create_droplet_now(droplet_params)
        return helpers.droplet_data_json(droplet)
    else:
        print(p_text("Configuration declined!"))
