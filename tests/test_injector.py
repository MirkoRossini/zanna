import unittest
from zanna import Injector
from unittest.mock import MagicMock
from zanna import Bindings
from unittest.mock import MagicMock

class TestBindings(unittest.TestCase):
    def test_init_empty(self):
        self.assertRaises(TypeError, Injector)
    
    def test_init_module_is_called(self):
        module = MagicMock()
        module.side_effect = self._called_with_bindings
        Injector(module)
        assert module.called

    @staticmethod
    def _called_with_bindings(bindings):
        assert isinstance(bindings, Bindings)
