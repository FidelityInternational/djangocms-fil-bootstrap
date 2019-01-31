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

Alternatively, specifying `--all` will use all predefined data sources (roles, demo).
