

from ._binding_spec import BindingSpec
from typing import Type
from inspect import isclass


class ClassBindingSpec(BindingSpec):
    """
    Binding spec for a class.
    """
    def __init__(self, klass:Type):
        self._validate_argument(klass)
   
    @staticmethod
    def _validate_argument(argument):
        if not isclass(argument):
            raise TypeError(
                "{} should only be used with classes".format(
                    ClassBindingSpec.__name__))
