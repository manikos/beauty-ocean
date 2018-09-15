=====
Usage
=====

``beauty_ocean`` was designed to be used not only as a cli command (via the
excellent python library `click <https://github.com/pallets/click>`_) but
also as a function call as well.
Assuming that ``beauty_ocean`` is already installed inside your virtualenv's
dev-dependencies (or globally) then in your terminal:

.. code-block:: console

    $ droplet

    # or
    $ droplet --token DIGITAL_OCEAN_API_TOKEN_ENV_NAME

    # or
    $ droplet --token path/to/file/that/holds/the/token

    # or
    $ droplet --token THE_ACTUAL_API_TOKEN_HERE

    # want help?
    $ droplet --help


``beauty_ocean`` accepts one option ``-t`` (short version) or
``--token`` (long version) which can either be:

1. an environment variable name which holds the DigitalOcean API Token (default: ``DO_TOKEN``)
2. a file name (which contains only the DigitalOcean API Token) or
3. the actual DigitalOcean API Token itself

The recommended way to use this tool is to provide an environment variable
name to the ``--token`` option. If the option is omitted, ``beauty_ocean``
will look in your environment variables for ``DO_TOKEN``.
If not found, it will raise a ``ValueError``.

The steps that ``beauty_ocean`` takes to resolve to an API Token are described
below, by priority:

Assuming that you entered: ``droplet -t ABCDEF`` then:

1. it will look for an env var named ``"ABCDEF"``.
2. fail that, it will look for a file in the current dir named ``"ABCDEF"``
3. fail that, it will use the string ``"ABCDEF"`` as the DigitalOcean API Token


Once, a valid token is provided then ``beauty_ocean`` will initiate a list
of questions like the droplet's region, image, size, name etc and once all
these questions have been answered, a final confirmation dialog will be
displayed in order to create the droplet.

Finally, a json string will be returned with all the droplet data at your
disposal to use it in any way you want.

DEMO
----

.. raw:: html

    <video controls src="_static/new_demo.mp4"></video>


I built this tool to enhance automation of Digital Ocean's droplet(s).
Future work will include the extension of this tool to automate DNS and Networks.