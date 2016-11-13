from typing import Any, Dict, Iterable, Callable
from inspect import signature, Signature, Parameter, isclass
import builtins

from ._argument_spec import ArgumentSpec
from ._binding_spec import BindingSpec

_BUILTINS = set(builtin
                for builtin in builtins.__dict__.values()
                if isclass(builtin))


def _isbuiltin_class(klass: type):
    return klass in _BUILTINS


def _arg_has_valid_annotation(arg: Parameter):
    return arg.annotation != Signature.empty \
           and not _isbuiltin_class(arg.annotation)


def get_argument_specs_for_callable(callable_obj: Callable):
    return [ArgumentSpec(
        arg.annotation if _arg_has_valid_annotation(arg) else None, name)
            for name, arg in signature(callable_obj).parameters.items()
            if name != 'self']


class ProviderBindingSpec(BindingSpec):
    """
    Binding spec for a provider.
    """

    def __init__(self, provider: Callable):
        self._validate_argument(provider)
        self._provider = provider
        self._argument_specs = get_argument_specs_for_callable(provider)

    @staticmethod
    def _validate_argument(argument):
        if not callable(argument):
            raise TypeError(
                "{} should only be used with callables".format(
                    ProviderBindingSpec.__name__))

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
        return self._provider(**keyword_arguments)

    def get_argument_specs(self) -> Iterable[ArgumentSpec]:
        return self._argument_specs
