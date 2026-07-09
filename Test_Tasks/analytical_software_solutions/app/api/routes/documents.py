from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import ElasticDep, SessionDep
from app.schemas.documents import DeleteDocumentResponse, DocumentSearchResponse
from app.search.documents import ElasticsearchUnavailableError
from app.services.documents import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/search", response_model=DocumentSearchResponse)
async def search_documents(
    session: SessionDep,
    es: ElasticDep,
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=20),
) -> DocumentSearchResponse:
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must not be empty.",
        )

    service = DocumentService(session=session, es=es)
    try:
        documents = await service.search(q=q, limit=limit)
    except ElasticsearchUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search engine is unavailable.",
        ) from exc

    return DocumentSearchResponse(items=documents)


@router.delete("/{document_id}", response_model=DeleteDocumentResponse)
async def delete_document(
    document_id: int,
    session: SessionDep,
    es: ElasticDep,
) -> DeleteDocumentResponse:
    service = DocumentService(session=session, es=es)
    try:
        deleted = await service.delete(document_id=document_id)
    except ElasticsearchUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search engine is unavailable.",
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DeleteDocumentResponse(id=document_id, deleted=True)
