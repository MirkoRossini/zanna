import unittest
from unittest.mock import MagicMock

from zanna import Injector
from zanna import Binder

THING_VALUE = 3
OTHERTHING_VALUE = 30


class ThingConsumer:
    def __init__(self, thing):
        assert thing == THING_VALUE


class ClassConsumer:
    def __init__(self, thing_consumer: ThingConsumer):
        assert isinstance(thing_consumer, ThingConsumer)


class JustAClass:
    pass


def provider(otherthing):
    assert otherthing == OTHERTHING_VALUE
    return THING_VALUE


def just_a_class_provider(otherthing) -> JustAClass:
    assert otherthing == OTHERTHING_VALUE
    return JustAClass()


class TestInjector(unittest.TestCase):
    def test_init_empty(self):
        self.assertRaises(TypeError, Injector)

    def test_init_module_is_called(self):
        module = MagicMock()
        module.side_effect = self._called_with_binder

        Injector(module)
        assert module.called

        other_module1 = MagicMock()
        other_module2 = MagicMock()
        other_module1.side_effect = self._called_with_binder
        other_module2.side_effect = self._called_with_binder

        module.reset_mock()

        Injector(module, other_module1, other_module2)
        assert module.called
        assert other_module1.called
        assert other_module2.called

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

    def test_get_instance_using_type(self):
        def module(binder):
            binder.bind(ThingConsumer)
            binder.bind(ClassConsumer)
            binder.bind_to("thing", THING_VALUE)

        i = Injector(module)
        class_consumer = i.get_instance(ClassConsumer)
        assert class_consumer is not None
        assert isinstance(class_consumer, ClassConsumer)

    def test_get_instance_using_type_without_binding(self):
        def module(binder):
            binder.bind(ThingConsumer)
            binder.bind_to("thing", THING_VALUE)

        i = Injector(module)
        class_consumer = i.get_instance(ClassConsumer)
        assert isinstance(class_consumer, ClassConsumer)

    def test_get_instance_fallback_name(self):
        def module(binder):
            binder.bind_to("thing_consumer", ThingConsumer)
            binder.bind(ClassConsumer)
            binder.bind_to("thing", THING_VALUE)

        i = Injector(module)
        class_consumer = i.get_instance(ClassConsumer)
        assert class_consumer is not None
        assert isinstance(class_consumer, ClassConsumer)

    def test_get_instance_with_provider(self):
        def module(binder):
            binder.bind(ThingConsumer)
            binder.bind_provider("thing", provider)
            binder.bind_to("otherthing", OTHERTHING_VALUE)

        i = Injector(module)
        thing_consumer = i.get_instance(ThingConsumer)
        assert thing_consumer is not None
        assert isinstance(thing_consumer, ThingConsumer)

    def test_get_instance_with_provider_using_annotation(self):
        def module(binder):
            binder.bind_provider(just_a_class_provider)
            binder.bind_to("otherthing", OTHERTHING_VALUE)

        i = Injector(module)
        just_a_class = i.get_instance(JustAClass)
        assert just_a_class is not None
        assert isinstance(just_a_class, JustAClass)

    def test_is_singleton_by_default(self):
        def module(binder):
            binder.bind(JustAClass)

        i = Injector(module)
        just_a_class = i.get_instance(JustAClass)
        assert just_a_class is not None
        assert isinstance(just_a_class, JustAClass)
        just_a_class_now = i.get_instance(JustAClass)
        assert just_a_class is just_a_class_now

    @staticmethod
    def _called_with_binder(binder):
        assert isinstance(binder, Binder)
