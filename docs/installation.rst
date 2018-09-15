.. highlight:: shell

============
Installation
============


Stable release (preferred method)
---------------------------------

To install beauty-ocean, run this command in your terminal (**do not run this
command using sudo**, instead create a virtualenv. If you can't create one,
install it inside your ``~/.local/`` dir using ``pip install --user beauty-ocean``):

.. code-block:: console

    (virtualenv_name) $ pip install beauty-ocean

This is the preferred method to install ``beauty-ocean``, as it will **not**
interfere with your system packages and in addition it will always be the
most recent stable release.

If you don't have `pip`_ installed (which is very unlikely if you are under
a virtualenv), this `Python installation guide`_ can guide you through the process.


From sources
------------

The sources for beauty-ocean can be downloaded from the `Github repo`_.

You can either install it directly from the public repository:

.. code-block:: console

    $ pip install git+https://github.com/manikos/beauty-ocean.git

Or download and install the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/manikos/beauty-ocean/tarball/master
    $ pip install manikos-beauty-ocean-<commit_hash>.tar.gz


.. _pip: https://pip.pypa.io/en/stable/installing/
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Github repo: https://github.com/manikos/beauty-ocean
.. _tarball: https://github.com/manikos/beauty_ocean/tarball/master