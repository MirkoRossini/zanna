import unittest

import pytest

from zanna._argument_spec import ArgumentSpec
from zanna._provider_binding_spec import ProviderBindingSpec


def provider(value) -> str:
    return "{value} {value}".format(value=value)


def provider_empty() -> str:
    return " "


class DummyProvider(object):
    def __call__(self, value) -> str:
        return provider(value)


class TestProviderBindingSpec(unittest.TestCase):
    def test_binding_instance_raises(self):
        with pytest.raises(TypeError):
            ProviderBindingSpec(3)
        with pytest.raises(TypeError):
            ProviderBindingSpec("")

    def test_has_instance_is_null_at_beginning(self):
        assert not ProviderBindingSpec(provider).has_instance()
        with pytest.raises(TypeError):
            ProviderBindingSpec(provider).get_instance()

    def test_get_argument_specs(self):
        class_binding_spec = ProviderBindingSpec(provider)
        assert class_binding_spec.get_argument_specs() == [
            ArgumentSpec(None, "value")]

    def test_get_argument_specs_specs_empty(self):
        class_binding_spec = ProviderBindingSpec(provider_empty)
        assert class_binding_spec.get_argument_specs() == []

    def test_construct_instance(self):
        with pytest.raises(TypeError):
            ProviderBindingSpec(provider).construct_instance({})
        assert ProviderBindingSpec(provider).construct_instance(
            {"value": 3}) == "3 3"

    def test_construct_instance_provider_instance(self):
        dummy_provider = DummyProvider()
        with pytest.raises(TypeError):
            ProviderBindingSpec(dummy_provider).construct_instance({})
        assert ProviderBindingSpec(dummy_provider).construct_instance(
            {"value": 3}) == "3 3"
