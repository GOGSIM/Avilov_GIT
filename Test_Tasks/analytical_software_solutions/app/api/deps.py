from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.search.client import get_elasticsearch

SessionDep = Annotated[AsyncSession, Depends(get_session)]
ElasticDep = Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]
