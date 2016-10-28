from typing import Callable, Iterable, Union, Any
from ._default_binder import _DefaultBinder
from ._binder import Binder


class Injector(object):
    def __init__(self, module: Callable[[Binder], None], *othermodules: Iterable[Callable[[Binder], None]]):
        self._binder = _DefaultBinder()
        module(self._binder)
        for othermodule in othermodules:
            othermodule(self._binder)

    def get_instance(self, string_or_class: Union[type, str]) -> Any:
        binding_spec = self._binder.get_binding(string_or_class)
        if binding_spec.has_instance():
            return binding_spec.get_instance()
        else:
            return self._construct_instance(binding_spec)

    def _construct_instance(self, binding_spec):
        argument_specs = binding_spec.get_argument_specs()
        return binding_spec.construct_instance({arg.name: self._get_instance_for_argument_spec(arg) for arg in argument_specs})

    def _get_instance_for_argument_spec(self, argument_spec):
        if argument_spec.type is None:
            return self.get_instance(argument_spec.name)
        try:
            return self.get_instance(argument_spec.type)
        except ValueError:
            return self.get_instance(argument_spec.name)
