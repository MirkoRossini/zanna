from typing import Any, Dict, Iterable
from inspect import isclass

from ._binding_spec import BindingSpec
from ._argument_spec import ArgumentSpec
from ._provider_binding_spec import get_argument_specs_for_callable


def get_argument_specs_for_class(klass: type):
    if not isinstance(klass, type):
        raise TypeError("klass should be a type")
    return get_argument_specs_for_callable(klass)


class ClassBindingSpec(BindingSpec):
    """
    Binding spec for a class.
    """

    def __init__(self, klass: type):
        self._validate_argument(klass)
        self._klass = klass
        self._argument_specs = get_argument_specs_for_class(klass)

    @staticmethod
    def _validate_argument(argument):
        if not isclass(argument):
            raise TypeError(
                "{} should only be used with classes".format(
                    ClassBindingSpec.__name__))

    def has_instance(self):
        """
        Instances must be constructed each time,
        so we will never have an instance ready to be retrieved
        """
        return False

    def get_instance(self) -> Any:
        """
        Should never be called, instances are constructed each time.
        """
        raise TypeError(
            ("{} doesn't have ready to use instances, "
             "they need to be constructed each time").format(
                self.__class__.__name__))

    def construct_instance(self, keyword_arguments: Dict[str, object]) -> Any:
        return self._klass(**keyword_arguments)

    def get_argument_specs(self) -> Iterable[ArgumentSpec]:
        return self._argument_specs
