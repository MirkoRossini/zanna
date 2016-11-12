from collections import namedtuple
from typing import Union, Callable, Iterable

from ._binder import Binder

BIND_PROVIDER = 'bind_provider'
BIND = 'bind'

_MethodCall = namedtuple('_MethodCall', ['method_name', 'args'])


class _MethodCallsListModule:
    def __init__(self):
        self._methodcalls = []

    def add_method_call(self, method_name: str, args: Iterable):
        self._methodcalls.append(_MethodCall(method_name, args))

    def __call__(self, binder: Binder) -> None:
        for method_name, args in self._methodcalls:
            getattr(binder, method_name)(*args)


_module = _MethodCallsListModule()


def provider_for(class_or_string: Union[type, str] = None) -> Callable:
    def bind_provider(provider):
        _module.add_method_call(BIND_PROVIDER, (class_or_string, provider))
        return provider

    return bind_provider


def provider(provider: Callable) -> None:
    _module.add_method_call(BIND_PROVIDER, (provider,))


def inject(klass: type) -> type:
    _module.add_method_call(BIND, (klass,))
    return klass
