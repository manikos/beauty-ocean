============
beauty-ocean
============

.. image:: https://img.shields.io/readthedocs/beauty-ocean.svg?style=flat-square
        :target: `full documentation on ReadTheDocs`_
        :alt: ReadTheDocs documentation status

.. image:: https://img.shields.io/pypi/v/beauty-ocean.svg?style=flat-square
        :target: https://pypi.org/project/beauty-ocean/
        :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/manikos/beauty-ocean/master.svg?style=flat-square
        :target: https://travis-ci.org/manikos/beauty-ocean/
        :alt: Travis CI build status

.. image:: https://img.shields.io/codecov/c/github/manikos/beauty-ocean.svg?style=flat-square
        :target: https://codecov.io/gh/manikos/beauty-ocean/
        :alt: Codecov status

.. image:: https://img.shields.io/pypi/pyversions/beauty-ocean.svg?style=flat-square
        :target: https://pypi.org/project/beauty-ocean/
        :alt: Supported Python versions

.. image:: https://img.shields.io/github/license/manikos/beauty-ocean.svg?style=flat-square
        :target: https://github.com/manikos/beauty-ocean/bolb/master/LICENSE
        :alt: Project's licence



Create DigitalOcean droplets like a breeze through the command line.


Documentation
-------------
You may read the `full documentation on ReadTheDocs`_.


Preparation
-----------
Before installing this package make sure you have an account to
`Digital Ocean <https://www.digitalocean.com>`_ and have
`obtained a Digital Ocean API token <https://www.digitalocean.com/docs/api/create-personal-access-token/>`_
The recommended way of storing the token is via environment variable. Once
you copy it, do the following:


.. code-block:: console

    $ vim ~/.profile or nano ~/.profile
    # make sure the following line is added
    $ export DO_TOKEN="API TOKEN HERE"  # or other name than DO_TOKEN
    $ source ~/.profile


Installation
------------
Installation is just a `pip install` away:

.. code-block:: console

    (virtualenv_name) $ pip install beauty-ocean

You are using virtualenv, don't you? If not, install it inside your
``~/.local`` directory.

.. code-block:: console

    $ pip install --user beauty-ocean

`Never ever use sudo! <https://youtu.be/5BqAeN-F9Qs?t=8m42s>`_


Usage
-----
For the moment, this package implements the creation of
`Digital Ocean droplets <https://www.digitalocean.com/products/droplets/>`_
but very soon it will support the creation of Domains and Networks.
Once installed, the ``droplet`` command will be available at your disposal.
It accepts a single option ``--token`` or ``-t`` for short. Defaults to
``"DO_TOKEN"`` which is the name of the environment variable that you
created earlier. If you used a different name then pass that name to the
``-t`` option.

.. code-block:: console

    $ droplet

    # or
    $ droplet -t MY_ENV_NAME_FOR_TOKEN

You may, also, pass a file path to the ``-t`` option where this file holds
the token only.

.. code-block:: console

    $ droplet --t path/to/file/that/holds/the/token

Lastly, **but not recommended**, you may pass directly, to the ``-t`` option,
the token itself.

.. code-block:: console

    $ droplet --t THE_ACTUAL_API_TOKEN_HERE

Once the token is resolved, a series of questions will be initiated in order
to get the available data from you, submit this data to the Digital Ocean
API and create the droplet. All the above come in a good-looking format
of questions.

Finally, a json string will be returned with all the droplet data at your
disposal to use it in any way you want.


Features
--------
* Beautiful command-line-interface questions flow with sensible defaults
* Supports remote or local SSH keys addition and/or remote/local Tags


Demo
----
An mp4 video demo can be found `here <https://beauty-ocean.readthedocs.io/en/latest/usage.html#demo>`_.


Credits
-------
This package was created using:

* Cookiecutter_
* `audreyr/cookiecutter-pypackage`_ project template
* python-digitalocean_ python library for DigitalOcean API
* inquirer_ to ask questions (based on the inquirejs_ command line UI)
* colored_ to color the prompt
* yaspin_ to display a "loading" animation while fetching data
* click_ to create the command line
* sshpubkeys_ to parse/validate public key(s)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _inquirer: https://github.com/magmax/python-inquirer
.. _inquirejs: https://github.com/SBoudrias/Inquirer.js
.. _python-digitalocean: https://github.com/koalalorenzo/python-digitalocean
.. _colored: https://gitlab.com/dslackw/colored
.. _yaspin: https://github.com/pavdmyt/yaspin
.. _click: https://github.com/pallets/click
.. _sshpubkeys: https://github.com/ojarva/python-sshpubkeys
.. _full documentation on ReadTheDocs: https://readthedocs.org/projects/beauty-ocean/


Disclaimer
----------
I do not work at DigitalOcean, neither have any benefits (financial or
professional) from creating this package. This package was created because
it facilitates my workflow during droplet creation and website deployment
and I wanted to share it with other developers. Sharing is a good thing!
