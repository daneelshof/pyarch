import abc
from typing import Generic, TypeVar
from entity import Entity as DomainEntity, EntityId

Entity = TypeVar("Entity", bound=DomainEntity)


class GenericRepository(Generic[EntityId, Entity], metaclass=abc.ABCMeta):
    """an interface for the repository pattern"""

    @abc.abstractmethod
    def get_by_id(self, id: EntityId) -> Entity:
        raise NotImplementedError()

