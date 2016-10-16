import unittest
from zanna._default_bindings import _DefaultBindings
from unittest.mock import MagicMock


class DummyClass():
    pass

def dummyfunc():
    pass

class TestDefaultBindings(unittest.TestCase):
    def setUp(self):
        self.bindings = _DefaultBindings()
    def test_can_bind_nonclass_raises(self):
        self.assertRaises(TypeError, self.bindings.bind, "")
        self.assertRaises(TypeError, self.bindings.bind_to, 1, "")
    def test_can_bind_by_name(self):
        self.bindings.bind_to("instance", [])
    def test_cannot_bind_twice(self):
        self.bindings.bind_to("instance", [])
        self.assertRaises(ValueError, self.bindings.bind_to, "instance", 21)
    
    
    def test_can_bind_by_class(self):
        self.bindings.bind_to(DummyClass, [])
    def test_can_bind_class(self):
        self.bindings.bind(DummyClass)
    def test_can_bind_function(self):
        self.bindings.bind_to("name", dummyfunc)
    def test_can_bind_mocks(self):
        self.bindings.bind_to(DummyClass, MagicMock())