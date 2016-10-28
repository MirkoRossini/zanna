from typing import Callable, Iterable, Union, Any
from ._default_binder import _DefaultBinder


class Injector(object):
    def __init__(self, module: Callable, *othermodules: Iterable[Callable]):
        self._binder = _DefaultBinder()
        module(self._binder)

    def get_instance(self, string_or_class: Union[type, str]) -> Any:
        binding_spec = self._binder.get_binding(string_or_class)
        if binding_spec.has_instance():
            return binding_spec.get_instance()
        
        return None
        
