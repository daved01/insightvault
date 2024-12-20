import uuid
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document model

    Attributes:
        id: str
        title: str
        content: str
        metadata: dict[str, Any]
        embedding: list[float] | None
        created_at: datetime
        updated_at: datetime
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    metadata: Mapping[str, Any] = Field(default_factory=dict)
    embedding: Sequence[float] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
