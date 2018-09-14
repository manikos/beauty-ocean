import json
from pprint import pprint
from typing import List, Union

from sshpubkeys import SSHKey as SSHPubKey
from digitalocean import SSHKey, Manager, Droplet

from beauty_ocean.core import config, helpers
from beauty_ocean.droplet import api
from beauty_ocean.droplet import questions


def validate_public_key(path: str) -> Union[str, None]:
    """
    :param str path: path to the public key
    :return: str or None
    """
    pub_key = helpers.read_path(path)
    ssh = SSHPubKey(pub_key, strict=True)
    if ssh.parse() is None:
        return pub_key


def post_public_key(token: str, public_key: str) -> List[SSHKey]:
    """
    Given the API token and the public key, posts the public key to
    the account.

    :param str token: the API token
    :param str public_key: the public key
    :return: a list of one element digitalocean.SSHKey
    """
    name = questions.ask_for_public_key_name()
    ssh_key = SSHKey(token=token, name=name, public_key=public_key)

    # Post the ssh key to DO in order to get an ssh key id
    ssh_key = api.create_ssh_key(ssh_key)
    return [ssh_key]


def handle_ssh_keys(manager: Manager, addition_method: str) -> list:
    """
    Post local public key to DO account or select one or more ssh keys
    that are already present on DO account.

    :param digitalocean.Manager.Manager manager: instance
    :param str addition_method: the chosen addition method (remote|local)
    :return: list (of zero or more digitalocean.SSHKey.SSHKey instances)
    """
    msg = "Enter the path to your public key"
    if addition_method == "remote":  # go get remote ssh keys
        remote_ssh_keys = questions.ask_for_remote_ssh_keys_selection(manager)
        if remote_ssh_keys:
            return remote_ssh_keys
        else:
            msg = f"No ssh keys selected or found on DO! {msg}"
    path = questions.ask_for_public_key_path(msg)
    public_key = validate_public_key(path)
    if public_key:
        return post_public_key(manager.token, public_key)
    return []


def handle_tag_selection(manager: Manager, both: bool = False) -> list:
    """
    Handles tag selection

    :param digitalocean.Manager.Manager manager: instance
    :param boolean both: whether or not both remote + new tags to be added
    :return: list (of zero or more strings)
    """
    tags = questions.ask_for_remote_tag_selection(manager)
    if not tags:
        message = (
            f"No remote tags found {config.SORRY}! {questions.NEW_TAG_MSG}"
        )
        return questions.ask_for_new_tag(message=message)
    if both:
        tags += questions.ask_for_new_tag()
    return tags


def handle_tags(manager, addition_method: str) -> list:
    """
    Given an addition method, adds corresponding tag(s).

    :param digitalocean.Manager.Manager manager: instance
    :param str addition_method: the tag addition method
    :return: list (of zero or more strings)
    """
    if addition_method == "remote":
        return handle_tag_selection(manager)
    elif addition_method == "new":
        return questions.ask_for_new_tag()
    else:  # some/all remote and some new tags will be added
        return handle_tag_selection(manager, both=True)


def padding_text(s: str, length: int=60, pad: str="-") -> str:
    """
    Centers the given str between a padding form (total length is "length").
    Example (str = "Hello", length=11, pad="+"):
        +++HELLO+++
    :param str s: the string to center
    :param int length: number of characters (incl. pad)
    :param str pad: the padding character
    :return: str
    """
    return f"\n{s.upper().center(length, pad)}\n"


def review_droplet_data(data: dict) -> None:
    """
    Pretty print the data dictionary that contains droplet's configuration.

    :param dict data: droplet data to be submitted
    :return: None
    """
    exclude = "token"
    to_review = {k: v for k, v in data.items() if k != exclude}
    print(config.cyan_text(padding_text("Droplet configuration")))
    pprint(to_review, indent=4, width=10)
    print(config.cyan_text(padding_text("End droplet configuration")))


def create_droplet_now(droplet_params) -> Droplet:
    """
    Given some droplet parameters, make an API call in order to create
    the Droplet.

    :param dict droplet_params: droplet (selected) parameters
    :return: digitalocean.Droplet instance
    """
    # create a Droplet instance
    bare_droplet = Droplet(**droplet_params)

    # initialize it (to get the id)
    pre_droplet = api.boot_droplet(bare_droplet)

    # poll it in order to know when it'll be ready-to-go
    print(config.green_text("Droplet initialized! Booting..."))
    droplet = api.poll_droplet(pre_droplet)
    print(config.green_text("Droplet has been created successfully! \(´▽`)/"))
    return droplet


def filter_droplet_return_data(droplet: Droplet) -> dict:
    """
    Creates a new dict that contains valuable data from the newly created
    Droplet. Discards sensitive data such as "token" and any logs.

    :param digitalocean.Droplet.Droplet droplet: instance
    :return: dict
    """
    to_return = {}
    black_list = ["token", "_log"]
    for key, value in vars(droplet).items():
        if key in black_list:
            continue
        elif key == "ssh_keys":
            to_return["ssh_keys"] = [key.name for key in value]
        else:
            to_return[key] = value
    return to_return


def droplet_data_json(droplet: Droplet) -> str:
    """
    Return a JSON representation of a (properly formatted) droplet.

    :param digitalocean.Droplet.Droplet droplet: instance
    :return: str (json)
    """
    to_return = filter_droplet_return_data(droplet)
    return json.dumps(to_return)
