************************
django CMS FIL Bootstrap
************************

========
Overview
========

django CMS FIL Bootstrap allows users to load initial set of data into the database.
It can be used to create user groups, setup permissions and more.

============
Installation
============

Requirements
============

django CMS FIL Bootstrap requires that you have a django CMS 4.0 (or higher) project already running and set up.


To install
==========

Run::

    pip install djangocms-fil-bootstrap

Add ``djangocms_fil_bootstrap`` to your project's ``INSTALLED_APPS``.


=====
Usage
=====

Run::

    python manage.py bootstrap (<file> <file>|--all)

Where ``file`` is one of predefined data sources (for example: ``demo``, or ``roles``),
or path to your own data source.

Alternatively, specifying ``--all`` will use all predefined data sources (roles, demo).


============
Architecture
============

Addon consists of multiple :class:`djangocms_fil_bootstrap.components.Component` classes.

Each component specifies a ``field_name``, which is a key in the data source where the component's data is located.

This data is then put in component's instance attribute called ``raw_data``. Component's ``parse`` method can then access that data.

Component can specify a ``default_factory``, which is a function that generates default value for the ``raw_data`` if the key doesn't exist in the source file.

Example:

a-json-file.json

.. code-block:: json

    {
      "users": ["bar", "baz"]
    }

.. code-block:: python

    from django.contrib.auth.models import User
    from djangocms_fil_bootstrap.components import Components

    class NewUsers(Component):
        field_name = "users"
        default_factory = list

        def parse(self):
            for user in self.raw_data:
                User.objects.create(username=user, password=user)

```NewUsers`` must be added to a list of components executed in :func:`djangocms_fil_bootstrap.bootstrap`.

