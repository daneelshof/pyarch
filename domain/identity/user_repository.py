import uuid
from sqlalchemy import Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.schema import Column

from infrastructure.sqlalchemy import Base


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text(), unique=True, nullable=False)
    email = Column(Text(), unique=True, nullable=False)
    password_hash = Column(Text(), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    is_admin = Column(Boolean(), nullable=False)
