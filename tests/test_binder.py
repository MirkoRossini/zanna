import unittest
from unittest.mock import MagicMock

from zanna._default_binder import _DefaultBinder
from zanna._binding_spec import InstanceBindingSpec
from zanna._singleton_class_binding_spec import SingletonClassBindingSpec


class DummyClass():
    pass


def dummyfunc():
    pass


class TestDefaultBinder(unittest.TestCase):
    def setUp(self):
        self.binder = _DefaultBinder()

    def test_bind_nonclass_raises(self):
        self.assertRaises(TypeError, self.binder.bind, "")
        self.assertRaises(TypeError, self.binder.bind_to, 1, "")

    def test_can_bind_by_name(self):
        self.binder.bind_to("instance", [])

    def test_get_binding_nonclass_or_string_raises(self):
        self.assertRaises(TypeError, self.binder.get_binding, 1)

    def test_can_bind_provider(self):
        class Dummy:
            pass

        def provider() -> Dummy:
            pass

        self.binder.bind_provider(provider)

    def test_binding_non_callable_provider_raises(self):
        def provider():
            pass

        self.assertRaises(TypeError, self.binder.bind_provider, "provider", 1)
        self.assertRaises(TypeError, self.binder.bind_provider, "provider")
        self.assertRaises(TypeError, self.binder.bind_provider, provider)
        self.binder.bind_provider("provider", provider)

    def test_cannot_bind_twice(self):
        self.binder.bind_to("instance", [])
        self.assertRaises(ValueError, self.binder.bind_to, "instance", 21)

    def test_can_bind_by_class(self):
        self.binder.bind_to(DummyClass, [])

    def test_can_bind_class(self):
        self.binder.bind(DummyClass)

    def test_can_override_binding(self):
        self.binder.bind(DummyClass)
        self.binder.override_binding(DummyClass, [])

    def test_can_bind_function(self):
        self.binder.bind_to("name", dummyfunc)

    def test_can_bind_mocks(self):
        self.binder.bind_to(DummyClass, MagicMock())

    def test_raises_if_not_bound(self):
        self.assertRaises(ValueError, self.binder.get_binding, "instance")

    def test_correct_binding_specs_are_set_up(self):
        self.binder.bind_to("instance", [])
        self.binder.bind(DummyClass)
        assert self.binder.get_binding("instance") != []
        assert isinstance(self.binder.get_binding("instance"),
                          InstanceBindingSpec)
        assert isinstance(self.binder.get_binding(DummyClass),
                          SingletonClassBindingSpec)
