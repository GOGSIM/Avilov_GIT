import argparse
import asyncio
import json
from pathlib import Path

from app.config import get_settings
from app.db.session import async_session_factory
from app.logging_config import configure_logging
from app.main import app
from app.search.client import get_elasticsearch
from app.search.documents import DocumentSearchIndex
from app.services.consistency import check_consistency
from app.services.import_csv import import_csv


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    parser = argparse.ArgumentParser(description="Document search service commands.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import-csv")
    import_parser.add_argument("path", type=Path)

    subparsers.add_parser("reindex")
    subparsers.add_parser("check-consistency")

    openapi_parser = subparsers.add_parser("export-openapi")
    openapi_parser.add_argument("--output", type=Path, default=Path("docs.json"))

    args = parser.parse_args()

    if args.command == "import-csv":
        asyncio.run(_import_csv(args.path))
    elif args.command == "reindex":
        asyncio.run(_reindex())
    elif args.command == "check-consistency":
        asyncio.run(_check_consistency())
    elif args.command == "export-openapi":
        _export_openapi(args.output)


async def _import_csv(path: Path) -> None:
    async with async_session_factory() as session:
        async for es in get_elasticsearch():
            result = await import_csv(path=path, session=session, es=es)
            print(
                "Import complete: "
                f"read={result.read}, saved={result.saved}, "
                f"indexed={result.indexed}, skipped={result.skipped}"
            )


async def _reindex() -> None:
    from app.repositories.documents import DocumentRepository

    async with async_session_factory() as session:
        async for es in get_elasticsearch():
            repository = DocumentRepository(session)
            search_index = DocumentSearchIndex(es)
            await search_index.recreate_index()

            indexed = 0
            async for batch in repository.iter_batches():
                indexed += await search_index.index_documents(batch)

            print(f"Reindex complete: indexed={indexed}")


async def _check_consistency() -> None:
    async with async_session_factory() as session:
        async for es in get_elasticsearch():
            report = await check_consistency(session=session, es=es)
            print(f"Postgres documents: {report.postgres_count}")
            print(f"Elasticsearch documents: {report.elasticsearch_count}")
            print(f"Missing in index: {len(report.missing_in_index)}")
            print(f"Missing in db: {len(report.missing_in_db)}")
            print(f"Status: {'ok' if report.is_consistent else 'inconsistent'}")


def _export_openapi(output: Path) -> None:
    output.write_text(
        json.dumps(app.openapi(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OpenAPI schema exported to {output}")


if __name__ == "__main__":
    main()
