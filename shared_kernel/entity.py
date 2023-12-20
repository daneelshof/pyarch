from dataclasses import dataclass, field
from typing import Generic, TypeVar
from shared_kernel import GenericUUID

EntityId = TypeVar("EntityId", bound=GenericUUID)

@dataclass
class Entity(Generic[EntityId]):
    """A base class for entities"""
    id: EntityId = field(hash=True)

    @classmethod
    def next_id(cls) -> EntityId:
        return GenericUUID.next_id()