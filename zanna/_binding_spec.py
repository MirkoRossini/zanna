
from typing import Any
from inspect import isfunction, isclass


class BindingSpec(object):
    def __init__(self, bound_object: Any):
        self._spec = None
        if self._needs_spec(bound_object):
            self._instance = None
            raise Exception()
        else:
            self._instance = bound_object

    def get_instance(self):
        return self._instance
            
    def _needs_spec(self, bound_object: Any) -> bool:
        return isclass(bound_object) or isfunction(bound_object)


