=====
zanna
=====


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
==========

Zanna is meant to be a modern (3.5+), well maintained injection library for Python.


Features
========

* Support for typing annotations
* Decorators are not mandatory: all the injection logic can be outside your modules
* Supports injection by name
* Instances can be bound directly, useful when testing (i.e. by override bindings with mocks)
* No autodiscover for performance reasons and to avoid running into annoying bugs

Usage
=====

Injecting by variable name
--------------------------

The basic form of injection is performed by variable name.
The injector expects a list of modules (any callable that takes a Binder as argument).
You can get the bound instance by calling get_instance

..  code-block:: python

    from zanna import Injector, Binder

    def mymodule(binder: Binder) -> None:
        binder.bind_to("value", 3)

    injector = Injector(mymodule)
    assert injector.get_instance("value") == 3

Zanna will automatically inject the value into arguments with the same name:

..  code-block:: python

    from zanna import Injector, Binder

    def mymodule(binder: Binder) -> None:
        binder.bind_to("value", 3)

    class ValueConsumer:
        def __init__(self, value):
            self.value = value

    injector = Injector(mymodule)
    assert injector.get_instance(ValueConsumer).value == 3


Injecting by type annotation
----------------------------

Zanna also makes use of python typing annotations to find the right instance to inject.

..  code-block:: python

    from zanna import Injector, Binder

    class ValueClass:
        def __init__(self, the_value: int):
            self.the_value = the_value

    class ValueConsumer:
        def __init__(self, value_class_instance: ValueClass):
            self.value_class_instance = value_class_instance

    def mymodule(binder: Binder) -> None:
        binder.bind_to("the_value", 3)
        binder.bind(ValueClass)

    injector = Injector(mymodule)
    assert injector.get_instance(ValueConsumer).value_class_instance.the_value == 3


Singleton or not singleton?
---------------------------

Instances provided by the injector are always singletons, meaning that the __init__ method of
the class will be called only the first time, and every subsequent call of get_instance will
return the same instance:

..  code-block:: python

    from zanna import Injector

    class MyClass:
        pass
    injector = Injector(lambda binder: binder.bind(MyClass))
    assert injector.get_instance(MyClass) == injector.get_instance(MyClass)



Use providers for more complex use cases
----------------------------------------

Binder instances can be used to bind providers. A provider is any callable that takes
any number of arguments and returns any type. The injector will try to inject all the necessary
arguments. Providers can be bound explicitely or implicitely (in which case zanna will use the
return annotation to bind by type).

..  code-block:: python

    from zanna import Injector, Binder

    class AValueConsumer:
        def __init__(self, value: int):
            self.value = value

    def explicit_provider(a_value: int) -> int:
        return a_value + 100

    def implicit_provider(value_plus_100: int) -> AValueConsumer:
        return AValueConsumer(value_plus_100)

    def mymodule(binder: Binder) -> None:
        binder.bind_to("a_value", 3)
        binder.bind_provider("value_plus_100", explicit_provider)
        binder.bind_provider(implicit_provider)

    injector = Injector(mymodule)
    assert injector.get_instance(AValueConsumer).value == 103


Override existing bindings
--------------------------

Bindings can be overridden. Overriding a non-existent binding will result in a ValueError being raised.

Override bindings is extremely useful when testing, as any part of your stack can be replaced with a mock.


..  code-block:: python

    from zanna import Injector, Binder
    from unittest.mock import MagicMock

    class ValueClass:
        def __init__(self):
            pass
        def retrieve_something(self):
            return ['some', 'thing']

    class ValueConsumer:
        def __init__(self, value: ValueClass):
            self.value = value


    def mymodule(binder: Binder) -> None:
        binder.bind(ValueClass)

    injector = Injector(mymodule)
    assert injector.get_instance(ValueConsumer).value.retrieve_something() == ['some', 'thing']

    def module_overriding_value_class(binder: Binder) -> None:
        mock_value_class = MagicMock(ValueClass)
        mock_value_class.retrieve_something.return_value = ['mock']
        binder.override_binding(ValueClass, mock_value_class)

    injector = Injector(mymodule, module_overriding_value_class)
    assert injector.get_instance(ValueConsumer).value.retrieve_something() == ['mock']


Using the decorators
--------------------

One of the advantages of using Zanna over other solutions is that it doesn't force you
to pollute your code by mixing in the injection logic.

If you are working on a small project and would like to handle part (or all) of the
injection logic using decorators instead of modules, Zanna supports that as well.

Internally, Zanna creates a module that sets up the bindings as indicated by the decorators
(in a random order).

All Injectors initialized with use_decorators=True will run that module first on their Binder.

Zanna supports the following decorators:

* decorators.provider, which takes a provided annotated with an appropriate return type
* decorators.provider_for, which can be given the name or the class of the instance provided
* decorators.inject, to annotate class to be bound/injected

Here's an example:

..  code-block:: python

    from zanna import Injector
    from zanna import decorators
    class Thing:
        pass

    @decorators.provider_for("value")
    def provide_value():
        return 3

    @decorators.provider
    def provide_thing() -> Thing:
        return Thing()


    @decorators.inject
    class OtherThing:
        def __init__(self, value, thing:Thing):
            self.value = value
            self.thing = thing

    inj = Injector(use_decorators=True)
    otherthing = inj.get_instance(OtherThing)
    assert otherthing.value == 3
    assert isinstance(otherthing.thing, Thing)
    assert isinstance(otherthing, OtherThing)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

