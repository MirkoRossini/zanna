import unittest

import pytest

from zanna._argument_spec import ArgumentSpec
from zanna._class_binding_spec import ClassBindingSpec


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


class DummyClassWithType(object):
    def __init__(self, dummy: DummyClass):
        self._dummy = dummy


class TestClassBindingSpec(unittest.TestCase):
    def test_binding_instance_raises(self):
        with pytest.raises(TypeError):
            ClassBindingSpec(3)
        with pytest.raises(TypeError):
            ClassBindingSpec("")
        with pytest.raises(TypeError):
            ClassBindingSpec(DummyClass(""))

    def test_has_instance_is_null_at_beginning(self):
        assert not ClassBindingSpec(DummyClass).has_instance()
        with pytest.raises(TypeError):
            ClassBindingSpec(DummyClass).get_instance()

    def test_get_argument_specs(self):
        class_binding_spec = ClassBindingSpec(DummyClass)
        assert class_binding_spec.get_argument_specs() == [
            ArgumentSpec(None, "value")]

    def test_get_argument_specs_int_annotation(self):
        class_binding_spec = ClassBindingSpec(DummyClassIntAnnotation)
        self.assertEquals(class_binding_spec.get_argument_specs(), [
            ArgumentSpec(None, "value")])

    def test_get_argument_specs_type(self):
        class_binding_spec = ClassBindingSpec(DummyClassWithType)
        assert class_binding_spec.get_argument_specs() == [
            ArgumentSpec(DummyClass, "dummy")]

    def test_get_argument_specs_specs_empty(self):
        class_binding_spec = ClassBindingSpec(DummyClassEmpty)
        assert class_binding_spec.get_argument_specs() == []

    def test_construct_instance(self):
        assert ClassBindingSpec(DummyClassEmpty).construct_instance(
            {}) == DummyClassEmpty()
        with pytest.raises(TypeError):
            ClassBindingSpec(DummyClass).construct_instance({})
        assert ClassBindingSpec(DummyClass).construct_instance(
            {"value": 3}) == DummyClass(3)

    def test_get_instance(self):
        with pytest.raises(TypeError):
            ClassBindingSpec(DummyClass).get_instance()
