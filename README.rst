************************
django CMS FIL Bootstrap
************************

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

    python manage.py bootstrap <file>

Where ``file`` is one of predefined data sources (for example: ``demo``, or ``roles``).

You can also provide your own data source by specifying ``-e`` argument::

    python manage.py bootstrap -e <path>
