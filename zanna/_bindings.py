from typing import Union, Type, Text, Any
from abc import ABCMeta, abstractmethod



class Binder(metaclass=ABCMeta):
    @abstractmethod
    def bind(self, klass: type) -> None:
        pass

    @abstractmethod
    def bind_to(self, class_or_string: Union[type, str], bound_object: Any) -> None:
        pass
