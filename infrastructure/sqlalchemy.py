from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from sqlalchemy.orm import DeclarativeBase, Session
from shared_kernel.entity import Entity
from shared_kernel.exceptions import EntityNotFoundException
from shared_kernel.generic_repository import GenericRepository
from shared_kernel.generic_uuid import GenericUUID

MapEntityType = TypeVar("MapEntityType", bound=Entity)
MapModelType = TypeVar("MapModelType", bound=Any)


class Base(DeclarativeBase):
    pass


class EntityMapper(Generic[MapEntityType, MapModelType], ABC):
    entity_class: type[MapEntityType]
    model_class: type[MapModelType]

    @abstractmethod
    def model_to_entity(self, instance: MapModelType) -> MapEntityType:
        raise NotImplementedError()

    @abstractmethod
    def entity_to_model(self, instance: MapEntityType) -> MapModelType:
        raise NotImplementedError()


class Removed:
    def __repr__(self) -> str:
        return "<Removed entity>"

    def __str__(self) -> str:
        return "<Removed entity>"


REMOVED = Removed()


class SqlAlchemyRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[EntityMapper[Entity, Base]]
    model_class: type[Entity]

    def __init__(self, session: Session, identity_map=None):
        self._session = session
        self._identity_map = identity_map or dict()

    def add(self, entity: Entity):
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_model(entity)
        self._session.add(instance)

    def remove(self, entity: Entity):
        self._check_not_removed(entity.id)
        self._identity_map[entity.id] = REMOVED
        instance = self._session.query(self.get_model_class()).get(entity.id)
        self._session.delete(instance)

    def remove_by_id(self, entity_id: GenericUUID):
        self._check_not_removed(entity_id)
        instance = self._session.query(self.get_model_class()).get(entity_id)
        if instance is None:
            raise EntityNotFoundException(repository=self, entity_id=entity_id)
        self._identity_map[entity_id] = REMOVED
        self._session.delete(instance)

    def get_by_id(self, entity_id: GenericUUID):
        instance = self._session.query(self.get_model_class()).get(entity_id)
        if instance is None:
            raise EntityNotFoundException(repository=self, entity_id=entity_id)
        return self._get_entity(instance)

    def persist(self, entity: Entity):
        self._check_not_removed(entity.id)
        assert(entity.id in self._identity_map), "Entity is not known to the repo. Be sure to first use add()"
        instance = self.map_entity_to_model(entity)
        merged = self._session.merge(instance)
        self._session.add(merged)

    def persist_all(self):
        """Persist all changes to all entities currently known to the repository"""
        for entity in self._identity_map.values():
            if entity is not REMOVED:
                self.persist(entity)

    @property
    def data_mapper(self):
        return self.mapper_class()

    def count(self) -> int:
        return self._session.query(self.model_class).count()

    def map_entity_to_model(self, entity: Entity):
        assert self.mapper_class, (
            f"No data mapper found for {self.__class__.__name__}"
            "Please include `mapper_class = ModelMapper` in the repository class"
        )

        return self.data_mapper.entity_to_model(entity)

    def map_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)

    def get_model_class(self):
        assert self.model_class is not None, (
            f"No model class in {self.__class__.__name__}"
            "Please include `model_class = Model` in the repository class"
        )

        return self.model_class


