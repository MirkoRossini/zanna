
from unittest import TestCase
from zanna._binding_spec import BindingSpec


class TestBindingSpect(TestCase):
    TEST_STRING = "testtest"
    def test_instance_binding_spec(self):
        
        bspec = BindingSpec(self.TEST_STRING)
        assert bspec.get_instance() == self.TEST_STRING
