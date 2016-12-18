import unittest

import pytest

from zanna._argument_spec import ArgumentSpec
from zanna._singleton_class_binding_spec import SingletonClassBindingSpec


class DummyClass(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, DummyClass):
            raise Exception()
        return other.value == self.value


class DummyClassIntAnnotation(object):
    def __init__(self, value: int):
        self.value = value


class DummyClassEmpty(object):
    def __init__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, DummyClassEmpty):
            raise Exception()
        return True


SINGLETON_CLASS_INITIALIZED = False


class IsSingletonTestClass:
    def __init__(self):
        global SINGLETON_CLASS_INITIALIZED
        if SINGLETON_CLASS_INITIALIZED:
            raise Exception("Already initialized!!")
        SINGLETON_CLASS_INITIALIZED = True


class DummyClassWithType(object):
    def __init__(self, dummy: DummyClass):
        self._dummy = dummy


class TestClassBindingSpec(unittest.TestCase):
    def test_binding_instance_raises(self):
        with pytest.raises(TypeError):
            SingletonClassBindingSpec(3)
        with pytest.raises(TypeError):
            SingletonClassBindingSpec("")
        with pytest.raises(TypeError):
            SingletonClassBindingSpec(DummyClass(""))

    def test_has_instance_is_false_at_beginning(self):
        assert not SingletonClassBindingSpec(DummyClass).has_instance()

    def test_get_argument_specs(self):
        class_binding_spec = SingletonClassBindingSpec(DummyClass)
        assert class_binding_spec.get_argument_specs() == [
            ArgumentSpec(None, "value")]

    def test_get_argument_specs_int_annotation(self):
        class_binding_spec = SingletonClassBindingSpec(DummyClassIntAnnotation)
        self.assertEquals(class_binding_spec.get_argument_specs(), [
            ArgumentSpec(None, "value")])

    def test_get_argument_specs_type(self):
        class_binding_spec = SingletonClassBindingSpec(DummyClassWithType)
        assert class_binding_spec.get_argument_specs() == [
            ArgumentSpec(DummyClass, "dummy")]

    def test_get_argument_specs_specs_empty(self):
        class_binding_spec = SingletonClassBindingSpec(DummyClassEmpty)
        assert class_binding_spec.get_argument_specs() == []

    def test_construct_instance(self):
        assert SingletonClassBindingSpec(DummyClassEmpty).construct_instance(
            {}) == DummyClassEmpty()
        with pytest.raises(TypeError):
            SingletonClassBindingSpec(DummyClass).construct_instance({})
        assert SingletonClassBindingSpec(DummyClass).construct_instance(
            {"value": 3}) == DummyClass(3)

    def test_get_instance(self):
        with pytest.raises(TypeError):
            SingletonClassBindingSpec(DummyClass).get_instance()

    def test_is_singleton(self):
        assert not SINGLETON_CLASS_INITIALIZED
        binding_spec = SingletonClassBindingSpec(IsSingletonTestClass)
        binding_spec.construct_instance({})
        assert SINGLETON_CLASS_INITIALIZED

        assert binding_spec.has_instance()
        # Will raise if IsSingletonTestClass init is called again
        assert isinstance(binding_spec.get_instance(), IsSingletonTestClass)
