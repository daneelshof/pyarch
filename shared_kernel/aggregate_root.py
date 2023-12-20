from dataclasses import dataclass, field
from shared_kernel import Entity, EntityId


@dataclass(kw_only=True)
class AggregateRoot(Entity[EntityId]):
    """Composite of one or more entities"""
