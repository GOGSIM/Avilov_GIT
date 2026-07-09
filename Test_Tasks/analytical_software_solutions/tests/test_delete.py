from unittest.mock import AsyncMock, patch

import pytest

from tests.conftest import make_document


@pytest.mark.asyncio
async def test_delete_removes_document_from_db_and_index(client):
    document = make_document(10, "text", 1)

    with patch("app.services.documents.DocumentSearchIndex") as index_cls:
        with patch("app.services.documents.DocumentRepository") as repository_cls:
            repository_cls.return_value.get_by_id = AsyncMock(return_value=document)
            repository_cls.return_value.delete_by_id = AsyncMock(return_value=True)
            index_cls.return_value.delete_document = AsyncMock(return_value=True)

            response = await client.delete("/api/v1/documents/10")

    assert response.status_code == 200
    assert response.json() == {"id": 10, "deleted": True}


@pytest.mark.asyncio
async def test_delete_returns_404_for_missing_document(client):
    with patch("app.services.documents.DocumentRepository") as repository_cls:
        repository_cls.return_value.get_by_id = AsyncMock(return_value=None)

        response = await client.delete("/api/v1/documents/404")

    assert response.status_code == 404
