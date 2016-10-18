from typing import Union, Any


class Binding(object):
    def __init__(self, class_or_string: Union[type, str], bound_object: Any):
        self.class_or_string = class_or_string
        self.bound_object = bound_object
