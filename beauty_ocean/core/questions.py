from digitalocean import Manager

from beauty_ocean.core import api, config


def confirm_account(manager: Manager) -> bool:
    """
    Given a manager (which is created from the API token) prompt for
    confirmation about using this account.
    :param Manager manager: instance
    :return: bool
    """
    account = api.get_account_data(manager)
    q = config.q_confirm(message=f"Continue as {account.email}", default=True)
    cont = config.answer(q)
    return cont
