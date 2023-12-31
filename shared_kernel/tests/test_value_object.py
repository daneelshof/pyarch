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

    def test_equality(self):
        value_object_one = ExampleValueObject(example_variable=15)
        value_object_two = ExampleValueObject(example_variable=15)
        assert value_object_one == value_object_two

    def test_inequality(self):
        value_object_one = ExampleValueObject(example_variable=55)
        value_object_two = ExampleValueObject(example_variable=90)
        assert value_object_one != value_object_two
