from dataclasses import dataclass
from shared_kernel.aggregate_root import AggregateRoot
from shared_kernel.generic_uuid import GenericUUID

UserId = GenericUUID


@dataclass
class User(AggregateRoot):
    id: UserId
    username: str
    email: str
    password_hash: str
    is_active: bool
    is_admin: bool

