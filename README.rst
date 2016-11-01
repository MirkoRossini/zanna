===============================
zanna
===============================


.. image:: https://img.shields.io/pypi/v/zanna.svg
        :target: https://pypi.python.org/pypi/zanna

.. image:: https://img.shields.io/travis/MirkoRossini/zanna.svg
        :target: https://travis-ci.org/MirkoRossini/zanna

.. image:: https://readthedocs.org/projects/zanna/badge/?version=latest
        :target: https://zanna.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mirkorossini/zanna/shield.svg
     :target: https://pyup.io/repos/github/mirkorossini/zanna/
     :alt: Updates

.. image:: https://pyup.io/repos/github/mirkorossini/zanna/python-3-shield.svg
     :target: https://pyup.io/repos/github/mirkorossini/zanna/
     :alt: Python 3

Simple Dependency Injection library.
Supports python 3.5+ and makes full use of the typing annotations.
The design is pythonic but inspired by Guice in many aspects.

* Free software: BSD license
* Documentation: https://zanna.readthedocs.io.

Motivation
----------

Zanna is meant to be a modern (3.5+), well maintained injection library for Python.


Features
--------

* Support for typing annotations
* Decorators are not mandatory: all the injection logic can be outside your modules
* Supports injection by name
* Instances can be bound directly, useful when testing (i.e. by override bindings with mocks)
* No autodiscover for performance reasons and to avoid running into annoying bugs



TODO
----

* Decorators
* Override bindings method

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

