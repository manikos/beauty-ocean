from digitalocean import Account, Manager

from beauty_ocean.core.config import pong, cyan_text


def get_account_data(manager: Manager) -> Account:
    """
    API call to DigitalOcean's API v2 in order to get account data.

    :param digitalocean.Manager.Manager manager: instance
    :return: digitalocean.Account.Account instance
    """
    with pong(text=cyan_text("Retrieving account data...")):
        return manager.get_account()
