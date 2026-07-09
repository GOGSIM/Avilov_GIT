from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    id: int
    rubrics: list[str]
    text: str
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentSearchResponse(BaseModel):
    items: list[DocumentRead]


class DeleteDocumentResponse(BaseModel):
    id: int
    deleted: bool
