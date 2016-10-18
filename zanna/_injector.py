from typing import Callable, Iterable, Union, Any
from ._default_binder import _DefaultBinder


class Injector(object):
    def __init__(self, module: Callable, *othermodules: Iterable[Callable]):
        self._binder = _DefaultBinder()
        module(self._binder)

    def get_instance(self, string_or_class: Union[type, str]) -> Any:
        return None
        
