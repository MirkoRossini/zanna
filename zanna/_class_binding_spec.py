

from ._binding_spec import BindingSpec
from typing import Type, Any, Dict
from inspect import isclass


class ClassBindingSpec(BindingSpec):
    """
    Binding spec for a class.
    """
    def __init__(self, klass:Type):
        self._validate_argument(klass)
   
    @staticmethod
    def _validate_argument(argument):
        if not isclass(argument):
            raise TypeError(
                "{} should only be used with classes".format(
                    ClassBindingSpec.__name__))

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
             "they need to be constructed each time").format(self.__class__.__name__))
    
    def construct_instance(self, kwargs: Dict[str, object]) -> Any:
        pass
