from typing import Any, Dict, Iterable, Callable
from inspect import signature, Signature

from ._argument_spec import ArgumentSpec
from ._binding_spec import BindingSpec


def get_argument_specs_for_callable(callable_obj: Callable):
    return [ArgumentSpec(
        arg.annotation if arg.annotation != Signature.empty else None, name)
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
