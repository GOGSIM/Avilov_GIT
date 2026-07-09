import csv
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.documents import DocumentRepository
from app.search.documents import DocumentSearchIndex

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"id", "rubrics", "text", "created_date"}


@dataclass(frozen=True)
class ImportResult:
    read: int
    saved: int
    indexed: int
    skipped: int


@dataclass(frozen=True)
class ParsedCsv:
    rows: list[dict[str, Any]]
    read: int
    skipped: int


async def import_csv(
    path: Path,
    session: AsyncSession,
    es: AsyncElasticsearch,
) -> ImportResult:
    parsed_csv = _read_rows(path)
    repository = DocumentRepository(session)
    search_index = DocumentSearchIndex(es)

    saved = await repository.upsert_many(parsed_csv.rows)
    await session.commit()
    indexed = await search_index.index_documents(parsed_csv.rows)

    return ImportResult(
        read=parsed_csv.read,
        saved=saved,
        indexed=indexed,
        skipped=parsed_csv.skipped,
    )


def _read_rows(path: Path) -> ParsedCsv:
    documents: list[dict[str, Any]] = []
    read = 0
    skipped = 0

    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        sample = csv_file.read(4096)
        csv_file.seek(0)
        dialect = _detect_dialect(sample)
        reader = csv.DictReader(csv_file, dialect=dialect)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - fieldnames
        if missing_columns:
            raise ValueError(f"CSV file is missing columns: {sorted(missing_columns)}")

        for line_number, row in enumerate(reader, start=2):
            read += 1
            try:
                documents.append(_normalize_row(row))
            except ValueError as exc:
                skipped += 1
                logger.warning("Skipping CSV line %s: %s", line_number, exc)

    if skipped:
        logger.info("Skipped %s invalid CSV rows.", skipped)
    return ParsedCsv(rows=documents, read=read, skipped=skipped)


def _detect_dialect(sample: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;")
    except csv.Error:
        return csv.excel


def _normalize_row(row: dict[str, str | None]) -> dict[str, Any]:
    raw_text = (row.get("text") or "").strip()
    if not raw_text:
        raise ValueError("empty text")

    return {
        "id": int(row.get("id") or ""),
        "rubrics": _parse_rubrics(row.get("rubrics") or ""),
        "text": raw_text,
        "created_date": _parse_datetime(row.get("created_date") or ""),
    }


def _parse_rubrics(raw_value: str) -> list[str]:
    value = raw_value.strip()
    if not value:
        return []

    if value.startswith("["):
        parsed = json.loads(value.replace("'", '"'))
        if not isinstance(parsed, list):
            raise ValueError("rubrics must be a list")
        return [str(item).strip() for item in parsed if str(item).strip()]

    return [part.strip() for part in value.split(",") if part.strip()]


def _parse_datetime(raw_value: str) -> datetime:
    value = raw_value.strip()
    if not value:
        raise ValueError("empty created_date")
    if value.endswith("Z"):
        value = f"{value[:-1]}+00:00"
    return datetime.fromisoformat(value)
