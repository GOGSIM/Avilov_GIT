from collections.abc import AsyncIterator

from elasticsearch import AsyncElasticsearch

from app.config import get_settings


async def get_elasticsearch() -> AsyncIterator[AsyncElasticsearch]:
    settings = get_settings()
    client = AsyncElasticsearch(settings.elasticsearch_url)
    try:
        yield client
    finally:
        await client.close()
