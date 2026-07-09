from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from app.services.import_csv import _read_rows, import_csv


def test_read_rows_parses_csv(tmp_path: Path):
    csv_path = tmp_path / "documents.csv"
    csv_path.write_text(
        "id,rubrics,text,created_date\n"
        '1,"news, analytics","hello search",2024-01-01T00:00:00+00:00\n',
        encoding="utf-8",
    )

    parsed_csv = _read_rows(csv_path)

    assert parsed_csv.rows[0]["id"] == 1
    assert parsed_csv.rows[0]["rubrics"] == ["news", "analytics"]
    assert parsed_csv.rows[0]["text"] == "hello search"
    assert parsed_csv.read == 1
    assert parsed_csv.skipped == 0


def test_read_rows_parses_excel_friendly_semicolon_csv(tmp_path: Path):
    csv_path = tmp_path / "documents.csv"
    csv_path.write_text(
        "id;rubrics;text;created_date\n"
        '1;"news, analytics";"текст для поиска";2024-01-01T00:00:00+00:00\n',
        encoding="utf-8-sig",
    )

    parsed_csv = _read_rows(csv_path)

    assert parsed_csv.rows[0]["id"] == 1
    assert parsed_csv.rows[0]["rubrics"] == ["news", "analytics"]
    assert parsed_csv.rows[0]["text"] == "текст для поиска"


@pytest.mark.asyncio
async def test_import_csv_saves_and_indexes_rows(tmp_path: Path):
    csv_path = tmp_path / "documents.csv"
    csv_path.write_text(
        "id,rubrics,text,created_date\n"
        '1,"news","hello search",2024-01-01T00:00:00+00:00\n',
        encoding="utf-8",
    )
    session = AsyncMock()
    es = AsyncMock()

    with patch("app.services.import_csv.DocumentRepository") as repository_cls:
        with patch("app.services.import_csv.DocumentSearchIndex") as index_cls:
            repository_cls.return_value.upsert_many = AsyncMock(return_value=1)
            index_cls.return_value.index_documents = AsyncMock(return_value=1)

            result = await import_csv(csv_path, session, es)

    assert result.saved == 1
    assert result.indexed == 1
    assert result.read == 1
    assert result.skipped == 0
    session.commit.assert_awaited_once()
