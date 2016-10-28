from unittest import TestCase

import pytest

from zanna._binding_spec import InstanceBindingSpec


class DummyClass(object):
    def __init__(self, value):
        self.value = value


def TEST_CALLABLE(x):
    return x + 500


class TestInstanceBindingSpec(TestCase):
    TEST_STRING = "testtest"
    TEST_INT = 9999
    TEST_DUMMY_INSTANCE = DummyClass(TEST_STRING)

    def test_instance_binding_spec(self):
        bspec = InstanceBindingSpec(self.TEST_STRING)
        assert bspec.get_instance() == self.TEST_STRING

    def test_int_instance_binding_spec(self):
        bspec = InstanceBindingSpec(self.TEST_INT)
        assert bspec.get_instance() == self.TEST_INT

    def test_dummyclass_instance_binding_spec(self):
        bspec = InstanceBindingSpec(self.TEST_DUMMY_INSTANCE)
        assert bspec.get_instance() == self.TEST_DUMMY_INSTANCE

    def test_class_binding_spec_raises(self):
        with pytest.raises(TypeError):
            InstanceBindingSpec(DummyClass)

    def test_none_binding_spec_raises(self):
        with pytest.raises(TypeError):
            InstanceBindingSpec(None)

    def test_argspec_methods_raise(self):
        bspec = InstanceBindingSpec(3)
        with pytest.raises(TypeError):
            bspec.construct_instance({})
        with pytest.raises(TypeError):
            bspec.get_argument_specs()

    def test_callable_binding_spec(self):
        bspec = InstanceBindingSpec(TEST_CALLABLE)
        print(bspec.get_instance())
        assert bspec.get_instance()(500) == 1000
