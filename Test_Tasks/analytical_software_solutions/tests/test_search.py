from unittest.mock import AsyncMock, patch

import pytest

from tests.conftest import make_document


@pytest.mark.asyncio
async def test_search_returns_documents_sorted_by_created_date(client):
    older = make_document(1, "python backend", 1)
    newer = make_document(2, "python search", 3)

    with patch("app.services.documents.DocumentSearchIndex") as index_cls:
        with patch("app.services.documents.DocumentRepository") as repository_cls:
            index_cls.return_value.search_ids = AsyncMock(return_value=[1, 2])
            repository_cls.return_value.get_by_ids = AsyncMock(return_value=[older, newer])

            response = await client.get("/api/v1/documents/search", params={"q": "python"})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()["items"]] == [2, 1]


@pytest.mark.asyncio
async def test_search_rejects_blank_query(client):
    response = await client.get("/api/v1/documents/search", params={"q": "   "})

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_search_rejects_limit_above_twenty(client):
    response = await client.get(
        "/api/v1/documents/search",
        params={"q": "python", "limit": 21},
    )

    assert response.status_code == 422
