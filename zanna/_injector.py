from typing import Callable, Iterable, Union
from ._default_bindings import _DefaultBinder


class Injector(object):
    def __init__(self, module: Callable, *othermodules: Iterable[Callable]):
        self._bindings = _DefaultBinder()
        module(self._bindings)

    def get_instance(self, string_or_class: Union[type, str]) -> Any:
        return None
        
