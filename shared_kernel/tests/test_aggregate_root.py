import pytest

from shared_kernel import ValueObject
from shared_kernel.aggregate_root import AggregateRoot
from shared_kernel.generic_uuid import GenericUUID
from dataclasses import dataclass


@dataclass(frozen=True)
class ExampleValueObject(ValueObject):
    example_variable: int
    is_active: bool = True


@dataclass(kw_only=True)
class ExampleAggregateRoot(AggregateRoot[GenericUUID]):
    member: ExampleValueObject


class TestAggregateRoot:
    def test_instantiation(self):
        aggregate_root = ExampleAggregateRoot(
            id=ExampleAggregateRoot.next_id(),
            member=ExampleValueObject(example_variable=99)
        )
        assert aggregate_root.member.example_variable == 99
