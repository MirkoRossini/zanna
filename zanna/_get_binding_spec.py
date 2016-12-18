from inspect import isclass
from typing import Any

from ._binding_spec import InstanceBindingSpec, BindingSpec
from ._class_binding_spec import ClassBindingSpec


def get_binding_spec(bound_object: Any) -> BindingSpec:
    if isclass(bound_object):
        return ClassBindingSpec(bound_object)
    else:
        return InstanceBindingSpec(bound_object)
