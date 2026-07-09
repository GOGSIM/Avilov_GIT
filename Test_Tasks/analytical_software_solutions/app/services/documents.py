import logging

from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document
from app.repositories.documents import DocumentRepository
from app.search.documents import DocumentSearchIndex

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, session: AsyncSession, es: AsyncElasticsearch) -> None:
        self.session = session
        self.repository = DocumentRepository(session)
        self.search_index = DocumentSearchIndex(es)

    async def search(self, q: str, limit: int = 20) -> list[Document]:
        document_ids = await self.search_index.search_ids(query=q, limit=limit)
        documents = await self.repository.get_by_ids(document_ids)

        found_ids = {document.id for document in documents}
        missing_ids = [document_id for document_id in document_ids if document_id not in found_ids]
        if missing_ids:
            logger.warning(
                "Elasticsearch returned ids missing in PostgreSQL: %s",
                missing_ids,
            )

        return sorted(documents, key=lambda document: document.created_date, reverse=True)

    async def delete(self, document_id: int) -> bool:
        document = await self.repository.get_by_id(document_id)
        if document is None:
            return False

        await self.repository.delete_by_id(document_id)
        await self.search_index.delete_document(document_id)
        await self.session.commit()
        return True
