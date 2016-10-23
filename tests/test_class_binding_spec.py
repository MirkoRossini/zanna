import unittest
import pytest
from zanna._argument_spec import ArgumentSpec
from zanna._binding import Binding
from zanna._class_binding_spec import ClassBindingSpec

class DummyClass(object):
    def __init__(self, value):
        self.value = value


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

    def test_get_binding_specs(self):
        class_binding_spec = ClassBindingSpec(DummyClass)
        assert class_binding_spec.get_argument_specs() == [ArgumentSpec(None, "value")]

    def test_get_argument_specs(self):
        with pytest.raises(TypeError):
           ClassBindingSpec(DummyClass).get_instance()
