from fastapi import APIRouter, status
from sqlalchemy import text

from app.api.deps import ElasticDep, SessionDep
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def healthcheck(session: SessionDep, es: ElasticDep) -> HealthResponse:
    postgres_status = "ok"
    elasticsearch_status = "ok"

    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        postgres_status = "error"

    try:
        await es.info()
    except Exception:
        elasticsearch_status = "error"

    status_value = (
        "ok"
        if postgres_status == "ok" and elasticsearch_status == "ok"
        else "degraded"
    )
    return HealthResponse(
        status=status_value,
        postgres=postgres_status,
        elasticsearch=elasticsearch_status,
    )
