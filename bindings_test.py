import unittest
from zanna import Bindings
from unittest.mock import MagicMock


class DummyClass():
    pass

def dummyfunc():
    pass

class BindingsTest(unittest.TestCase):
    def setUp(self):
        self.bindings = Bindings()
    def test_can_bind_nonclass_raises(self):
        self.assertRaises(ValueError, self.bindings.bind, "")
        self.assertRaises(ValueError, self.bindings.bind_to, 1, "")
"""
    def test_can_bind_by_name(self):
        self.bindings.bind_to("instance", [])
    
    def test_can_bind_by_class(self):
        self.bindings.bind_to(DummyClass, [])
    def test_can_bind_class(self):
        self.bindings.bind(DummyClass)
    def test_can_bind_function(self):
        self.bindings.bind_to("name", dummyfunc)
    def test_can_copy_bindings(self):
        other_bindings = self.bindings.copy()
        self.assertNotEqual(id(other_bindings), id(self.bindings))
    def test_can_bind_mocks(self):
        self.bindings.bind(MagicMock())
       """ 
