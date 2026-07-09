from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.documents import DocumentRepository
from app.search.documents import DocumentSearchIndex


@dataclass(frozen=True)
class ConsistencyReport:
    postgres_count: int
    elasticsearch_count: int
    missing_in_index: list[int]
    missing_in_db: list[int]

    @property
    def is_consistent(self) -> bool:
        return (
            self.postgres_count == self.elasticsearch_count
            and not self.missing_in_index
            and not self.missing_in_db
        )


async def check_consistency(
    session: AsyncSession,
    es: AsyncElasticsearch,
    sample_size: int = 100,
) -> ConsistencyReport:
    repository = DocumentRepository(session)
    search_index = DocumentSearchIndex(es)

    postgres_ids = set(await repository.list_ids(limit=sample_size))
    elasticsearch_ids = set(await search_index.ids_sample(limit=sample_size))

    return ConsistencyReport(
        postgres_count=await repository.count(),
        elasticsearch_count=await search_index.count(),
        missing_in_index=sorted(postgres_ids - elasticsearch_ids),
        missing_in_db=sorted(elasticsearch_ids - postgres_ids),
    )
