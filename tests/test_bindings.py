import unittest
from zanna._default_binder import _DefaultBinder
from unittest.mock import MagicMock


class DummyClass():
    pass

def dummyfunc():
    pass

class TestDefaultBinder(unittest.TestCase):
    def setUp(self):
        self.binder = _DefaultBinder()
    def test_can_bind_nonclass_raises(self):
        self.assertRaises(TypeError, self.binder.bind, "")
        self.assertRaises(TypeError, self.binder.bind_to, 1, "")
    def test_can_bind_by_name(self):
        self.binder.bind_to("instance", [])
    def test_cannot_bind_twice(self):
        self.binder.bind_to("instance", [])
        self.assertRaises(ValueError, self.binder.bind_to, "instance", 21)
    
    
    def test_can_bind_by_class(self):
        self.binder.bind_to(DummyClass, [])
    def test_can_bind_class(self):
        self.binder.bind(DummyClass)
    def test_can_bind_function(self):
        self.binder.bind_to("name", dummyfunc)
    def test_can_bind_mocks(self):
        self.binder.bind_to(DummyClass, MagicMock())
