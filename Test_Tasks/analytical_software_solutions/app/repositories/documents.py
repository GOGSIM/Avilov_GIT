from collections.abc import AsyncIterator, Sequence

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, document_id: int) -> Document | None:
        return await self.session.get(Document, document_id)

    async def get_by_ids(self, document_ids: Sequence[int]) -> list[Document]:
        if not document_ids:
            return []

        result = await self.session.scalars(
            select(Document).where(Document.id.in_(document_ids))
        )
        return list(result.all())

    async def iter_batches(self, batch_size: int = 500) -> AsyncIterator[list[Document]]:
        offset = 0
        while True:
            result = await self.session.scalars(
                select(Document)
                .order_by(Document.id)
                .offset(offset)
                .limit(batch_size)
            )
            batch = list(result.all())
            if not batch:
                break
            yield batch
            offset += batch_size

    async def upsert_many(self, documents: Sequence[dict]) -> int:
        if not documents:
            return 0

        stmt = insert(Document).values(list(documents))
        update_fields = {
            "rubrics": stmt.excluded.rubrics,
            "text": stmt.excluded.text,
            "created_date": stmt.excluded.created_date,
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=[Document.id],
            set_=update_fields,
        )
        await self.session.execute(stmt)
        return len(documents)

    async def delete_by_id(self, document_id: int) -> bool:
        result = await self.session.execute(
            delete(Document).where(Document.id == document_id)
        )
        return bool(result.rowcount)

    async def count(self) -> int:
        result = await self.session.scalar(select(func.count()).select_from(Document))
        return int(result or 0)

    async def list_ids(self, limit: int | None = None) -> list[int]:
        stmt = select(Document.id).order_by(Document.id)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.scalars(stmt)
        return list(result.all())
