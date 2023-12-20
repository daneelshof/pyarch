from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """A base class for a value object"""