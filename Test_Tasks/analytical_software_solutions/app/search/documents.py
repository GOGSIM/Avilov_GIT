import logging
from collections.abc import Sequence

from elasticsearch import ApiError, AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk

from app.config import get_settings
from app.db.models import Document
from app.search.mappings import DOCUMENT_INDEX_MAPPING

logger = logging.getLogger(__name__)


class ElasticsearchUnavailableError(RuntimeError):
    pass


class DocumentSearchIndex:
    def __init__(self, es: AsyncElasticsearch) -> None:
        self.es = es
        self.index_name = get_settings().elasticsearch_index

    async def ensure_index(self) -> None:
        try:
            exists = await self.es.indices.exists(index=self.index_name)
            if not exists:
                await self.es.indices.create(
                    index=self.index_name,
                    **DOCUMENT_INDEX_MAPPING,
                )
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc

    async def recreate_index(self) -> None:
        try:
            exists = await self.es.indices.exists(index=self.index_name)
            if exists:
                await self.es.indices.delete(index=self.index_name)
            await self.es.indices.create(index=self.index_name, **DOCUMENT_INDEX_MAPPING)
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc

    async def index_documents(self, documents: Sequence[Document | dict]) -> int:
        if not documents:
            return 0

        await self.ensure_index()
        actions = [
            {
                "_op_type": "index",
                "_index": self.index_name,
                "_id": _document_id(document),
                "id": _document_id(document),
                "text": _document_text(document),
            }
            for document in documents
        ]
        try:
            success_count, errors = await async_bulk(
                self.es,
                actions,
                raise_on_error=False,
                refresh=True,
            )
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc

        if errors:
            logger.warning("Some documents were not indexed: %s", errors[:3])
        return int(success_count)

    async def search_ids(self, query: str, limit: int) -> list[int]:
        await self.ensure_index()
        try:
            response = await self.es.search(
                index=self.index_name,
                query={"match": {"text": {"query": query}}},
                size=limit,
                source=["id"],
            )
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc

        return [
            int(hit["_source"]["id"])
            for hit in response.get("hits", {}).get("hits", [])
            if "id" in hit.get("_source", {})
        ]

    async def delete_document(self, document_id: int) -> bool:
        try:
            await self.es.delete(
                index=self.index_name,
                id=document_id,
                refresh=True,
            )
            return True
        except NotFoundError:
            logger.warning("Document %s was missing in Elasticsearch.", document_id)
            return False
        except ApiError as exc:
            raise ElasticsearchUnavailableError from exc

    async def count(self) -> int:
        try:
            response = await self.es.count(index=self.index_name)
        except NotFoundError:
            return 0
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc
        return int(response["count"])

    async def ids_sample(self, limit: int = 100) -> list[int]:
        try:
            response = await self.es.search(
                index=self.index_name,
                query={"match_all": {}},
                size=limit,
                source=["id"],
                sort=[{"id": {"order": "asc"}}],
            )
        except NotFoundError:
            return []
        except Exception as exc:
            raise ElasticsearchUnavailableError from exc

        return [
            int(hit["_source"]["id"])
            for hit in response.get("hits", {}).get("hits", [])
            if "id" in hit.get("_source", {})
        ]


def _document_id(document: Document | dict) -> int:
    return int(document["id"] if isinstance(document, dict) else document.id)


def _document_text(document: Document | dict) -> str:
    return str(document["text"] if isinstance(document, dict) else document.text)
