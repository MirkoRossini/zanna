from typing import Callable, Iterable
from ._default_bindings import _DefaultBindings


class Injector(object):
    def __init__(self, module: Callable, *othermodules: Iterable[Callable]):
        self._bindings = _DefaultBindings()
        module(self._bindings)
