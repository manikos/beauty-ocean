import sys
import click

from beauty_ocean.droplet.entry import create_droplet


@click.command()
@click.option(
    "-t",
    "--token",
    type=str,
    help="Digital Ocean API token",
)
def create_droplet_click(token):
    """
    Creates a droplet in your DigitalOcean account.

    Accepts one option (the Digital Ocean API token key).

    token: [env var name | path to file | token str] Resolved in that order.
    Example:

    droplet -t MY_TOKEN

    The above will first look at an environment variable named MY_TOKEN.
    Fail that, it'll look at a file named MY_TOKEN.
    Fail that, it'll use the str "MY_TOKEN" as the Digital Ocean API
    token (which will fail, obviously).
    If option omitted then it will look at DO_TOKEN env var.
    """
    res = create_droplet(token=token)
    if res:
        click.echo(res)
    return 0


if __name__ == "__main__":
    sys.exit(create_droplet_click())  # pragma: no cover
