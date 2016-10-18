import unittest
import pytest
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
         
