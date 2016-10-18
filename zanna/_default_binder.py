
from inspect import (isclass, isfunction)
from typing import Union, Any
from ._binder import Binder
from ._binding import Binding

class _DefaultBinder(Binder):
    def __init__(self):
        self._bindings_dict = {}

    def bind(self, klass: type) -> None:
        self._verify_is_class(klass)
        self._add_binding(klass, klass)

    def bind_to(self, class_or_string: Union[type, str], bound_object: Any) -> None:
        self._verify_is_class_or_string(class_or_string)
        self._add_binding(class_or_string, bound_object)

    def get_binding(self, class_or_string: Union[type, str]) -> Binding:
        return None
    
    def _add_binding(self, class_or_string, bound_object: Any) -> None:
        if class_or_string in self._bindings_dict:
             raise ValueError("{} is already bound".format(class_or_string))
        self._bindings_dict[class_or_string] = bound_object

    @staticmethod
    def _verify_is_class(klass: type) -> None:
        if not isclass(klass):
             raise TypeError("Argument of bind method should be a class")

    @classmethod
    def _verify_is_class_or_string(cls, class_or_string: Union[type, str]) -> None:
        if not isclass(class_or_string) and not cls._is_string(class_or_string):
             raise TypeError("Argument of bind_to method should be a class or a string")

    @classmethod
    def _is_string(cls, class_or_string: Union[type, str]) -> None:
        return isinstance(class_or_string, str)

