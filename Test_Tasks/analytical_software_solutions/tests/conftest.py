from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_elasticsearch, get_session
from app.main import app


class FakeSession:
    def __init__(self) -> None:
        self.documents: dict[int, Any] = {}
        self.committed = False

    async def commit(self) -> None:
        self.committed = True

    async def execute(self, statement: Any) -> Any:
        return None


class FakeElasticsearch:
    def __init__(self) -> None:
        self.indexed_ids: list[int] = []
        self.deleted_ids: list[int] = []

    async def info(self) -> dict[str, str]:
        return {"status": "ok"}

    async def close(self) -> None:
        return None


@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def fake_es() -> FakeElasticsearch:
    return FakeElasticsearch()


@pytest.fixture
async def client(fake_session: FakeSession, fake_es: FakeElasticsearch) -> AsyncIterator[AsyncClient]:
    async def override_session() -> AsyncIterator[FakeSession]:
        yield fake_session

    async def override_es() -> AsyncIterator[FakeElasticsearch]:
        yield fake_es

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_elasticsearch] = override_es

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

    app.dependency_overrides.clear()


class DocumentStub:
    def __init__(
        self,
        id: int,
        text: str,
        created_date: datetime,
        rubrics: list[str] | None = None,
    ) -> None:
        self.id = id
        self.text = text
        self.created_date = created_date
        self.rubrics = rubrics or ["test"]


def make_document(document_id: int, text: str, month: int) -> DocumentStub:
    return DocumentStub(
        id=document_id,
        text=text,
        created_date=datetime(2024, month, 1, tzinfo=UTC),
    )
