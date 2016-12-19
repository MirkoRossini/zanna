from inspect import isclass
from typing import Any

from ._binding_spec import InstanceBindingSpec, BindingSpec
from ._singleton_class_binding_spec import SingletonClassBindingSpec


def get_binding_spec(bound_object: Any) -> BindingSpec:
    if isclass(bound_object):
        return SingletonClassBindingSpec(bound_object)
    else:
        return InstanceBindingSpec(bound_object)
