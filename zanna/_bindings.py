from inspect import (isclass, isfunction)

class Bindings(object):
    def __init__(self):
        self._bindings_dict = {}

    def bind(self, klass):
        self._verify_is_class(klass)

    def bind_to(self, class_or_string, subject):
        self._verify_is_class_or_string(class_or_string)

    @staticmethod
    def _verify_is_class(klass):
        if not isclass(klass):
             raise ValueError("Argument of bind method should be a class")

    @classmethod
    def _verify_is_class_or_string(cls, class_or_string):
        if not isclass(class_or_string) and not cls._is_string(class_or_string):
             raise ValueError("Argument of bind_to method should be a class or a string")
    @classmethod
    def _is_string(cls, class_or_string):
        return isinstance(class_or_string, str)
