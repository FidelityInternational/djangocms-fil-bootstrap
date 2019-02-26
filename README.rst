************************
django CMS FIL Bootstrap
************************

========
Overview
========

django CMS FIL BootstrÊap allows users to load initial set of data into the database.
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
Each of these represents a Django model for which to import data.
Each of these extends the `components/base.py` Component class, which provides data accessors for 
each component via magic methods.

This allows you to then data from any key within any component by using: `self.bootstrap.data("other_key")`

Each component specifies a ``field_name``, which is a key in the data source where the component's data is located.

This data is then put in component's instance attribute called ``raw_data``. Component's ``parse`` method can then access that data.

Component can specify a ``default_factory``, which is a function that generates default value for the ``raw_data`` if the key doesn't exist in the source file.

Example:

a-json-file.json

:: 

    code-block:: json

    {
      "users": ["bar", "baz"]
    }

:: 

    code-block:: python

    from django.contrib.auth.models import User
    from djangocms_fil_bootstrap.components import Components

    class NewUsers(Component):
        field_name = "users"
        default_factory = list

        def parse(self):
            for user in self.raw_data:
                User.objects.create(username=user, password=user)

::

    `NewUsers must be added to a list of components executed in :func:
    djangocms_fil_bootstrap.bootstrap`.


==============
Data structure
==============
Note that it is possible to conform to DRY principles *to a degree*. If you wish to accumulate data, then records in later files will still need to be defined but they do not require all the data to be present, providing that your component uses `get_or_create` when generating new records.

E.g. Let's say you have two json files to import: `roles.json` and `demo.json`. You may define all the permissions and roles in the first file. Any records which may be required in the second just need their unique identifier property, so that `get_or_create` will execute a SELECT instead of an INSERT.

Note that each root key in your json data file must correspond by name with one of the components, `Component.field_name` attribute.
And the json data type (i.e. list or object) for a given root key should correspond to the `default_factory` 

Thus in `roles.json` you might have this structure:

:: 
    
    code-block:: json

    "roles": {
        "publisher": {
            "name": "Publisher Role",
            "group": "publisher",
            ... # other fields
        },


Then in `demo.json` you may wish to use that role for generating related data, in which case you simply need to provide the unique identifier:

:: 
    
    code-block:: json

    "roles": {
        "publisher": {
            # provide the unique identifier only
            "name": "Publisher Role",
        },

    "workflows": {
        "wf1": {
            "name": "Workflow 1",
            "is_default": true,
            "role":
                {
                    # then you can reference the role by it's json key
                    "role": "publisher",
                    "is_required": true,
                    "order": 3
                }
        },
        
-----------
Permissions
-----------
* Use `aliases` to create shortnames for permissions. The idea is if a permission is repeated more than once, use an alias instead.
* List each permission by group or user
