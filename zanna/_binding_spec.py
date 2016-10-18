
from typing import Any, Dict
from inspect import isfunction, isclass
import abc

def _needs_spec(bound_object: Any) -> bool:
    return isclass(bound_object) or isfunction(bound_object)

class BindingSpec(metaclass=abc.ABCMeta):

    def has_instance(self) -> bool:
        """
        Returns true if the binding spec have an 
        instance ready to be returned, False otherwise.
        """
        raise NotImplementedError()

    def get_instance(self) -> Any:
        """
        Returns the instance associated with the BindingSpec.
        If the instance is not ready (i.e. it's None)
        it raises a 
        """
        raise NotImplementedError()
    
    def construct_instance(keyword_arguments: Dict[str, object]) -> Any:
        """
        Constructs an instance of the bound object given a map of arguments
        """
        pass

class InstanceBindingSpec(BindingSpec):
    def __init__(self, bound_object: Any):
        if bound_object is None:
            raise TypeError("Binding None is not allowed")
        self._spec = None
        if _needs_spec(bound_object):
            raise TypeError(
                "{} should only be used with object instances.".format(
                    self.__class__.__name__))
        else:
            self._instance = bound_object

    def get_instance(self):
        return self._instance
            


