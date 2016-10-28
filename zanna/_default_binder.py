from inspect import isclass, isfunction
from typing import Union, Any, Callable

from pyflakes.checker import Binding

from ._binder import Binder
from ._binding_spec import InstanceBindingSpec
from ._class_binding_spec import ClassBindingSpec
from ._provider_binding_spec import ProviderBindingSpec
from ._argument_spec import ArgumentSpec


class _DefaultBinder(Binder):
    def __init__(self):
        self._bindings_dict = {}

    def bind(self, klass: type) -> None:
        self._verify_is_class(klass)
        self._add_binding(klass, klass)

    def bind_to(self,
                class_or_string: Union[type, str],
                bound_object: Any) -> None:
        self._verify_is_class_or_string(class_or_string)
        self._add_binding(class_or_string, bound_object)

    def bind_provider(self,
                      class_or_string: Union[type, str],
                      callable_obj: Callable) -> None:
        self._verify_is_callable(callable_obj)
        self._verify_not_bound(class_or_string)
        self._bindings_dict[class_or_string] = ProviderBindingSpec(
            callable_obj)

    def get_binding(self,
                    class_or_string: Union[type, str]) -> Binding:
        self._verify_is_class_or_string(class_or_string)
        if class_or_string not in self._bindings_dict:
            raise ValueError("{} is not bound".format(class_or_string))
        return self._bindings_dict[class_or_string]

    def _add_binding(self,
                     class_or_string: Union[type, str],
                     bound_object: Any) -> None:
        self._verify_not_bound(class_or_string)
        self._bindings_dict[class_or_string] = self._get_binding_spec(
            bound_object)

    def _get_binding_spec(self, bound_object: Any) -> ArgumentSpec:
        if isclass(bound_object):
            return ClassBindingSpec(bound_object)
        else:
            return InstanceBindingSpec(bound_object)

    def _verify_not_bound(self, class_or_string: Union[type, str]):
        if class_or_string in self._bindings_dict:
            raise ValueError("{} is already bound".format(class_or_string))

    @staticmethod
    def _verify_is_class(klass: type) -> None:
        if not isclass(klass):
            raise TypeError("Argument of bind method should be a class")

    @staticmethod
    def _verify_is_callable(callable_obj: Callable):
        if not isfunction(callable_obj):
            raise TypeError(
                "Argument of bind_provider method should be a callable")

    @classmethod
    def _verify_is_class_or_string(cls,
                                   class_or_string: Union[type, str]) -> None:
        if not isclass(class_or_string) and not cls._is_string(
                class_or_string):
            raise TypeError(
                "Argument of bind_to method should be a class or a string")

    @classmethod
    def _is_string(cls, class_or_string: Union[type, str]) -> None:
        return isinstance(class_or_string, str)
