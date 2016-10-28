import unittest
from unittest.mock import MagicMock

from zanna import Injector
from zanna import Binder


THING_VALUE = 3

class ThingConsumer:
    def __init__(self, thing):
        assert thing == THING_VALUE
class JustAClass:
    pass



class TestBinder(unittest.TestCase):
    def test_init_empty(self):
        self.assertRaises(TypeError, Injector)

    def test_init_module_is_called(self):
        module = MagicMock()
        module.side_effect = self._called_with_binder
        Injector(module)
        assert module.called

    def test_get_simple_instance(self):
        i = Injector(lambda binder: binder.bind_to("thing", THING_VALUE))
        thing = i.get_instance("thing")
        assert thing == THING_VALUE

    def test_get_instance_of_class(self):
        i = Injector(lambda binder: binder.bind(JustAClass))
        instance = i.get_instance(JustAClass)
        assert instance is not None
        assert isinstance(instance, JustAClass)

    def test_get_instance_of_class_with_missing_arg_raises(self):
        i = Injector(lambda binder: binder.bind(ThingConsumer))
        self.assertRaises(ValueError, i.get_instance, ThingConsumer)

    def test_get_instance_of_class_with_arg(self):
        def module(binder):
            binder.bind(ThingConsumer)
            binder.bind_to("thing", THING_VALUE)
        i = Injector(module)
        thing_consumer = i.get_instance(ThingConsumer)
        assert thing_consumer is not None
        assert isinstance(thing_consumer, ThingConsumer)

    @staticmethod
    def _called_with_binder(binder):
        assert isinstance(binder, Binder)
