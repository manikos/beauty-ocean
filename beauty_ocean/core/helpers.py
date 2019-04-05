import os

from digitalocean import Manager

from beauty_ocean.core.config import DEFAULT_ENV_NAME, SORRY


def get_token(token: str = None) -> str:
    """
    Tries to find the API token in different locations in the following order:
    1. As an environment variable (recommended)
    2. As a file (preferably a hidden one)
    3. As a plain string given when running "droplet -t <token>"

    :param str token: env var or path to file or the actual token itself
    :return:
    """
    if token is None:
        try:
            return os.environ[DEFAULT_ENV_NAME]
        except KeyError:
            err = f"Token not found in environment variable " \
                  f"{DEFAULT_ENV_NAME} {SORRY}."
            raise ValueError(err) from None
    if os.environ.get(token):
        return str(os.environ.get(token))
    if os.path.isfile(token):
        with open(token) as f:
            return f.read().rstrip("\n")  # remove \n at the end
    if token:
        return token
    err = f"Token was not found in any of the available locations " \
          f"(env var, file or string) {SORRY}"
    raise ValueError(err)


def create_manager(token):
    do_token = get_token(token)
    return Manager(token=do_token)


def read_path(path: str) -> str:
    """
    Given a filesystem path of a file, return its contents.
    :param str path: path to a file
    :return: str (contents of the file)
    """
    path = os.path.expanduser(path)
    with open(path, "r") as f:
        contents = f.read()
    return contents
