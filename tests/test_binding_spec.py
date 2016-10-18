
from unittest import TestCase
from zanna._binding_spec import InstanceBindingSpec
import pytest 

class DummyClass(object):
    def __init__(self, value):
        self.value = value


class TestInstanceBindingSpec(TestCase):
    TEST_STRING = "testtest"
    TEST_INT = 9999
    TEST_DUMMY_INSTANCE = DummyClass(TEST_STRING)
    TEST_CALLABLE = lambda x: x + 500

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
            bspec = InstanceBindingSpec(DummyClass)

    def test_none_binding_spec_raises(self):
        with pytest.raises(TypeError):
            bspec = InstanceBindingSpec(None)

    def test_callable_binding_spec(self):
        bspec = InstanceBindingSpec(self.TEST_CALLABLE)
        assert bspec.get_instance()(500) == 1000
