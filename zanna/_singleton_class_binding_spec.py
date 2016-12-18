from typing import Any, Dict, Iterable

from ._binding_spec import BindingSpec
from ._argument_spec import ArgumentSpec
from ._provider_binding_spec import get_argument_specs_for_callable
from zanna._class_binding_spec import ClassBindingSpec


def get_argument_specs_for_class(klass: type):
    if not isinstance(klass, type):
        raise TypeError("klass should be a type")
    return get_argument_specs_for_callable(klass)


class SingletonClassBindingSpec(BindingSpec):
    """
    Binding spec for a class.
    """

    def __init__(self, klass: type):
        self._class_binding_spec = ClassBindingSpec(klass)
        self._instance = None

    def has_instance(self):
        """
        Instances must be constructed each time,
        so we will never have an instance ready to be retrieved
        """
        return self._instance is not None

    def get_instance(self) -> Any:
        """
        Should never be called, instances are constructed each time.
        """
        if self._instance is None:
            raise TypeError(
                ("{} instance not ready, "
                 "it needs to be constructed with the construct_instance "
                 "method").format(
                    self.__class__.__name__))
        return self._instance

    def construct_instance(self, keyword_arguments: Dict[str, object]) -> Any:
        self._instance = self._class_binding_spec.construct_instance(
            keyword_arguments)
        return self._instance

    def get_argument_specs(self) -> Iterable[ArgumentSpec]:
        return self._class_binding_spec.get_argument_specs()
