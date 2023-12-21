import pytest
from shared_kernel.value_object import ValueObject
from pydantic.dataclasses import dataclass
from dataclasses import FrozenInstanceError


@dataclass(frozen=True)
class ExampleValueObject(ValueObject):
    example_variable: int


class TestValueObject:
    def test_immutability(self):
        value_object = ExampleValueObject(example_variable=11)
        with pytest.raises(FrozenInstanceError):
            value_object.example_variable = 13
        assert value_object.example_variable == 11
