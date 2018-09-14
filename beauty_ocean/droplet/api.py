from digitalocean import Droplet, SSHKey, Manager

from beauty_ocean.core.config import pong, cyan_text


def get_all_images(
    manager: Manager, image_type: str = "distribution", text=""
) -> list:
    """
    API call to DigitalOcean's API v2 in order to fetch available images per
    the selected image type.

    :param digitalocean.Manager.Manager manager: instance
    :param str image_type: "distribution" or "application" or "all"
    :param str text: a text to appear while fetching
    :return: list of digitalocean.Image.Image instances
    """
    text = text or f"Retrieving {image_type.lower()} images..."
    if image_type == "all":
        image_type = None
    with pong(text=cyan_text(text)):
        return manager.get_images(type=image_type)


def get_all_regions(manager: Manager) -> list:
    """
    API call to DigitalOcean's API v2 in order to fetch all regions.

    :param digitalocean.Manager.Manager manager: instance
    :return: list of digitalocean.Region.Region instances
    """
    with pong(text=cyan_text("Retrieving available regions...")):
        return manager.get_all_regions()


def get_all_sizes(manager: Manager) -> list:
    """
    API call to DigitalOcean's API v2 in order to fetch all sizes.

    :param digitalocean.Manager.Manager manager: instance
    :return: list of digitalocean.Size.Size instances
    """
    with pong(text=cyan_text("Retrieving available sizes...")):
        return manager.get_all_sizes()


def get_remote_ssh_keys(manager: Manager) -> list:
    """
    API call to DigitalOcean's API v2 in order to fetch ssh keys.

    :param digitalocean.Manager.Manager manager: instance
    :return: list of digitalocean.SSHKey.SSHKey instances
    """
    with pong(text=cyan_text("Retrieving public keys from your account...")):
        return manager.get_all_sshkeys()


def get_remote_tags(manager: Manager) -> list:
    """
    API call to DigitalOcean's API v2 in order to fetch all remote tags.

    :param digitalocean.Manager.Manager manager: instance
    :return: list of digitalocean.Tag.Tag instances
    """
    with pong(text=cyan_text("Retrieving existing tags...")):
        return manager.get_all_tags()


def create_ssh_key(ssh_key: SSHKey) -> SSHKey:
    """
    API call to DigitalOcean's API v2 in order to create the ssh key.

    :param digitalocean.SSHKey.SSHKey ssh_key: object
    :return: digitalocean.SSHKey.SSHKey
    """
    with pong(text=cyan_text("The SSH key is posted...")):
        ssh_key.create()
    return ssh_key


def boot_droplet(droplet: Droplet) -> Droplet:
    """
    API call to DigitalOcean's API v2 in order to initialize the droplet.
    This function will just "hit the switch-on button" on the server.
    During boot, the droplet is not considered as "created" yet.

    :param digitalocean.Droplet.Droplet droplet: instance
    :return: an instance of digitalocean.Droplet.Droplet
    """
    with pong(text=cyan_text("Your droplet is initializing...")):
        droplet.create()

    # droplet, now, has an id but not yet been fully created
    return droplet


def poll_droplet(droplet: Droplet, poll_interval: int = 4) -> Droplet:
    """
    Given a new-born droplet (without an IP), poll every poll_interval seconds
    the DO API in order to find out when the droplet is ready.

    :param digitalocean.Droplet.Droplet droplet: instance
    :param int poll_interval: get droplet status every poll_interval seconds
    :return: digitalocean.Droplet.Droplet instance or None
    """
    creation_action = droplet.get_action(droplet.action_ids[0])
    result = creation_action.wait(update_every_seconds=poll_interval)
    if result:
        # droplet is now fully created (with IP, tags etc)
        text = "Retrieving droplet data after boot..."
        with pong(text=cyan_text(text)):
            return droplet.load()
