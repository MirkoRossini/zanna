from typing import Any, Dict, Iterable
from inspect import isclass
import abc

from ._argument_spec import ArgumentSpec


def _needs_spec(bound_object: Any) -> bool:
    return isclass(bound_object)


class BindingSpec(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def has_instance(self) -> bool:
        """
        Returns true if the binding spec have an
        instance ready to be returned, False otherwise.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instance(self) -> Any:
        """
        Returns the instance associated with the BindingSpec.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def construct_instance(self, keyword_arguments: Dict[str, object]) -> Any:
        """
        Constructs an instance of the bound object given a map of arguments
        """
        pass

    @abc.abstractmethod
    def get_argument_specs(self) -> Iterable[ArgumentSpec]:
        """
        Returns the bindings necessary to construct the instance.
        """
        pass


class InstanceBindingSpec(BindingSpec):
    def __init__(self, bound_object: Any):
        self._validate_object(bound_object)
        self._instance = bound_object

    def get_instance(self):
        return self._instance

    def construct_instance(self, keyword_arguments: Dict[str, object]) -> Any:
        raise TypeError("{} doesn't need to construct instances".format(
            InstanceBindingSpec.__name__))

    def has_instance(self) -> bool:
        return True

    @staticmethod
    def _validate_object(bound_object: Any):
        if bound_object is None:
            raise TypeError("Binding None is not allowed")
        if _needs_spec(bound_object):
            raise TypeError(
                ("{} should only be used with object "
                 "instances and unbound callables.").format(
                    InstanceBindingSpec.__name__))

    def get_argument_specs(self) -> Iterable[ArgumentSpec]:
        raise TypeError("{} doesn't have any argument specs".format(
            InstanceBindingSpec.__name__))
