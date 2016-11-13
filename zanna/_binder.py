from typing import Union, Any, Callable
from abc import ABCMeta, abstractmethod


class Binder(metaclass=ABCMeta):
    @abstractmethod
    def bind(self, klass: type) -> None:
        pass

    @abstractmethod
    def bind_to(self,
                class_or_string: Union[type, str],
                bound_object: Any) -> None:
        pass

    @abstractmethod
    def bind_provider(self,
                      class_or_string: Union[type, str],
                      callable_obj: Callable) -> None:
        pass

    @abstractmethod
    def override_binding(self,
                         class_or_string: Union[type, str],
                         bound_object: Any) -> None:
        pass
