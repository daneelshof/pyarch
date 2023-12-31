from pydantic import BaseModel
from datetime import datetime


class DomainEvent(BaseModel):
    dateOccurred: datetime = datetime.now()

    def __next__(self):
        yield self


class CompositeDomainEvent(DomainEvent):
    events: list[DomainEvent]

    def __next__(self):
        yield from self.events
