import unittest
from unittest.mock import MagicMock

from zanna import Injector
from zanna import Binder


class TestBinder(unittest.TestCase):
    def test_init_empty(self):
        self.assertRaises(TypeError, Injector)

    def test_init_module_is_called(self):
        module = MagicMock()
        module.side_effect = self._called_with_binder
        Injector(module)
        assert module.called

    """
    def test_get_simple_instance(self):
        i = Injector(lambda binder: binder.bind_to("thing", 3))
        thing = i.get_instance("thing")
        assert thing == 3
    """
    """
    def test_get_instance(self):
        i = Injector(lambda binder: binder.bind_to("thing", 3))
        class ThingConsumer:
            def __init__(self, thing):
                assert thing == 3
        thing_consumer = i.get_instance(ThingConsumer)
        assert thing_consumer is not None
        assert isinstance(thing_consumer, ThingConsumer)
    """

    @staticmethod
    def _called_with_binder(binder):
        assert isinstance(binder, Binder)
