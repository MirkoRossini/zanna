
from unittest import TestCase
from zanna import Injector
from zanna import decorators

import pytest


class Thing:
    pass

@decorators.provider_for("value")
def provide_value():
    return 3

@decorators.provider
def provide_thing() -> Thing:
    return Thing()


@decorators.inject
class OtherThing:
    def __init__(self, value, thing:Thing):
        self.value = value
        self.thing = thing


class TestDecorators(TestCase):
    def test_provider_decorated_needs_type_or_name(self):
        with pytest.raises(TypeError):
            @decorators.provider
            def provider_invalid():
                pass
            inj = Injector(use_decorators=True)

    def test_provider_decorated(self):
        inj = Injector(use_decorators=True)
        assert inj.get_instance("value") == 3
        assert isinstance(inj.get_instance(Thing), Thing)

    def test_class_decorated(self):
        inj = Injector(use_decorators=True)
        otherthing = inj.get_instance(OtherThing)
        assert otherthing.value == 3
        assert isinstance(otherthing.thing, Thing)
        assert isinstance(otherthing, OtherThing)
