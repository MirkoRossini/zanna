from inspect import isclass
from typing import Any

from ._argument_spec import ArgumentSpec
from ._binding_spec import InstanceBindingSpec
from ._class_binding_spec import ClassBindingSpec


def get_binding_spec(bound_object: Any) -> ArgumentSpec:
    if isclass(bound_object):
        return ClassBindingSpec(bound_object)
    else:
        return InstanceBindingSpec(bound_object)
