from inspect import isclass, isfunction, signature
from typing import Union, Any, Callable

from ._binder import Binder
from ._provider_binding_spec import ProviderBindingSpec
from ._get_binding_spec import get_binding_spec
from ._binding_spec import BindingSpec


def _get_return_annotation_for_callable(callable_obj: Callable) -> type:
    sig = signature(callable_obj)
    if sig.return_annotation != sig.empty:
        return sig.return_annotation
    return None


class _DefaultBinder(Binder):
    def __init__(self):
        self._bindings_dict = {}

    def bind(self, klass: type) -> None:
        self._verify_is_class(klass)
        self.bind_to(klass, klass)

    def bind_to(self,
                class_or_string: Union[type, str],
                bound_object: Any) -> None:
        self._verify_is_class_or_string(class_or_string, 'bind_to')
        self._add_binding(class_or_string, bound_object)

    def bind_provider(self,
                      class_string_or_callable: Union[type, str, Callable],
                      callable_obj: Callable = None) -> None:
        if callable_obj is None:
            self._bind_provider_by_annotation(class_string_or_callable)

        else:
            self._verify_is_callable(callable_obj)
            self._verify_is_class_or_string(class_string_or_callable,
                                            'bind_provider')

            self._add_binding_spec(class_string_or_callable,
                                   ProviderBindingSpec(callable_obj))

    def get_binding(self,
                    class_or_string: Union[type, str]) -> BindingSpec:
        self._verify_is_class_or_string(class_or_string, 'get_binding')
        if class_or_string not in self._bindings_dict:
            if isinstance(class_or_string, str):
                raise ValueError("{} is not bound".format(class_or_string))
            return get_binding_spec(class_or_string)
        return self._bindings_dict[class_or_string]

    def _add_binding(self,
                     class_or_string: Union[type, str],
                     bound_object: Any) -> None:
        self._add_binding_spec(class_or_string, get_binding_spec(bound_object))

    def _add_binding_spec(self,
                          class_or_string: Union[type, str],
                          binding_spec: BindingSpec):
        self._verify_not_bound(class_or_string)
        self._bindings_dict[class_or_string] = binding_spec

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
                                   class_or_string: Union[type, str],
                                   method_name: str) -> None:
        if not isclass(class_or_string) and not cls._is_string(
                class_or_string):
            raise TypeError(
                "Argument of {} method should be a class or a string".format(
                    method_name))

    @classmethod
    def _is_string(cls, class_or_string: Union[type, str]) -> None:
        return isinstance(class_or_string, str)

    def _bind_provider_by_annotation(self, callable_obj):
        self._verify_is_callable(callable_obj)
        klass = _get_return_annotation_for_callable(
            callable_obj)
        if klass is None:
            raise TypeError("When binding a provider, "
                            "first argument must be a provider "
                            "with a return annotation")
        self.bind_provider(klass, callable_obj)

    def override_binding(self, class_or_string: Union[type, str],
                         bound_object: Any) -> None:
        self._verify_is_class_or_string(class_or_string, "override_binding")
        if class_or_string not in self._bindings_dict:
            raise ValueError(("{} is not bound "
                              "and can't be overridden").format(
                class_or_string))
        self._remove_binding(class_or_string)
        self._add_binding(class_or_string, bound_object)

    def _remove_binding(self, class_or_string: Union[type, str]):
        del self._bindings_dict[class_or_string]
