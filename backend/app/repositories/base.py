from typing import Protocol, TypeVar
from uuid import UUID

ModelT = TypeVar("ModelT")


class Repository[ModelT](Protocol):
    async def get(self, entity_id: UUID) -> ModelT | None:
        """Return one entity by identifier."""
