# Documents API

Небольшой сервис для поиска по текстам документов. Документы хранятся в
PostgreSQL, а Elasticsearch используется как отдельный поисковый индекс.

Проект сделан для тестового задания на позицию Junior Backend Python. Я старался
не усложнять архитектуру без необходимости: здесь есть рабочий API, импорт CSV,
переиндексация, миграции, Docker Compose и тесты для основных сценариев.

## Что умеет сервис

- искать документы по тексту;
- возвращать полные данные документа из PostgreSQL;
- сортировать результаты по `created_date DESC`;
- отдавать не больше 20 документов за один поисковый запрос;
- удалять документ по `id` из PostgreSQL и Elasticsearch;
- импортировать документы из CSV;
- пересобирать Elasticsearch-индекс из базы;
- проверять базовую консистентность между БД и индексом;
- отдавать healthcheck по PostgreSQL и Elasticsearch;
- хранить OpenAPI-схему в `docs.json`.

## Стек

| Зона | Инструмент |
| --- | --- |
| API | FastAPI |
| База данных | PostgreSQL |
| Поиск | Elasticsearch |
| ORM | SQLAlchemy 2.0 async |
| Миграции | Alembic |
| Настройки и схемы | Pydantic v2 |
| Запуск | Docker Compose |
| Тесты | pytest, httpx |
| Качество кода | ruff, black, mypy |

## Как это устроено

PostgreSQL здесь основное хранилище. В нем лежат все поля документа:
`id`, `rubrics`, `text`, `created_date`.

Elasticsearch хранит только то, что нужно для поиска: `id` и `text`. Поэтому
если индекс потеряется или устареет, его можно восстановить из PostgreSQL
командой `reindex`.

```text
             HTTP request
                  |
                  v
             FastAPI app
                  |
        +---------+---------+
        |                   |
        v                   v
  PostgreSQL          Elasticsearch
  id, rubrics,        id, text
  text, created_date
```

Поиск работает так:

1. Клиент отправляет строку поиска.
2. Elasticsearch ищет по `text` и возвращает id подходящих документов.
3. Сервис загружает полные документы из PostgreSQL.
4. Результат сортируется по `created_date DESC` и возвращается клиенту.

Удаление работает похожим образом: сначала проверяется документ в PostgreSQL,
потом запись удаляется из базы и из индекса.

## Структура проекта

```text
.
├── app/
│   ├── api/                # роуты FastAPI и зависимости
│   ├── db/                 # модели SQLAlchemy и подключение к БД
│   ├── repositories/       # запросы к PostgreSQL
│   ├── schemas/            # Pydantic-схемы
│   ├── search/             # работа с Elasticsearch
│   ├── services/           # основная бизнес-логика
│   ├── cli.py              # import-csv, reindex, check-consistency
│   ├── config.py
│   └── main.py
├── alembic/                # миграции
├── data/
│   └── sample.csv
├── tests/
├── docker-compose.yml
├── Dockerfile
├── docs.json
├── pyproject.toml
└── README.md
```

## Быстрый запуск

Собрать и запустить контейнеры:

```bash
docker compose up --build
```

После запуска нужно применить миграции:

```bash
docker compose exec api alembic upgrade head
```

И загрузить пример данных:

```bash
docker compose exec api python -m app.cli import-csv /app/data/sample.csv
```

API будет доступно здесь:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Переменные окружения

Для локального запуска через Docker достаточно значений из `.env.example`.

| Переменная | Описание | Значение по умолчанию |
| --- | --- | --- |
| `APP_NAME` | Название приложения | `Documents API` |
| `APP_ENV` | Имя окружения | `local` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |
| `DATABASE_URL` | Подключение к PostgreSQL | `postgresql+asyncpg://app:app@postgres:5432/documents` |
| `ELASTICSEARCH_URL` | Адрес Elasticsearch | `http://elasticsearch:9200` |
| `ELASTICSEARCH_INDEX` | Имя индекса | `documents` |

## Миграции

Применить миграции:

```bash
docker compose exec api alembic upgrade head
```

Таблица `documents`:

| Поле | Тип | Описание |
| --- | --- | --- |
| `id` | integer | id документа |
| `rubrics` | text array | список рубрик |
| `text` | text | текст документа |
| `created_date` | timestamp with timezone | дата создания |

## Импорт CSV

В репозитории есть пример:

```text
data/sample.csv
```

Импорт:

```bash
docker compose exec api python -m app.cli import-csv /app/data/sample.csv
```

Ожидаемые колонки:

| Колонка | Описание |
| --- | --- |
| `id` | уникальный id документа |
| `rubrics` | рубрики через запятую |
| `text` | текст документа |
| `created_date` | дата создания в ISO-формате |

При импорте документы сохраняются в PostgreSQL и сразу индексируются в
Elasticsearch.

## Переиндексация

Если нужно восстановить индекс из базы:

```bash
docker compose exec api python -m app.cli reindex
```

Команда пересоздает индекс и заново отправляет туда документы из PostgreSQL.
Для тестового проекта это простой и понятный вариант.

## Проверка консистентности

Команда сравнивает количество документов в PostgreSQL и Elasticsearch, а также
проверяет небольшую выборку id:

```bash
docker compose exec api python -m app.cli check-consistency
```

## API

| Метод | Путь | Что делает |
| --- | --- | --- |
| `GET` | `/health` | проверяет PostgreSQL и Elasticsearch |
| `GET` | `/api/v1/documents/search` | ищет документы по тексту |
| `DELETE` | `/api/v1/documents/{document_id}` | удаляет документ по id |

## Пример поиска

```bash
curl "http://localhost:8000/api/v1/documents/search?q=индекс&limit=20"
```

Пример ответа:

```json
{
  "items": [
    {
      "id": 3,
      "rubrics": ["archive"],
      "text": "Часть старых материалов перенесли в отдельный индекс для быстрого доступа.",
      "created_date": "2024-03-01T09:15:00Z"
    }
  ]
}
```

Параметры:

- `q` - поисковая строка, обязательный параметр;
- `limit` - количество документов, от 1 до 20.

## Пример удаления

```bash
curl -X DELETE "http://localhost:8000/api/v1/documents/3"
```

Ответ:

```json
{
  "id": 3,
  "deleted": true
}
```

Если документа нет в базе, вернется `404`.

## OpenAPI

Файл `docs.json` лежит в репозитории, потому что это есть в требованиях к
заданию.

Обновить его можно так:

```bash
docker compose exec api python -m app.cli export-openapi
```

Когда приложение запущено, схема доступна и по адресу:

```text
http://localhost:8000/openapi.json
```

## Тесты

Установить dev-зависимости:

```bash
pip install -e ".[dev]"
```

Запустить тесты локально:

```bash
pytest
```

Или внутри контейнера:

```bash
docker compose exec api pytest
```

Покрыты основные сценарии: поиск, сортировка, валидация запроса, удаление,
импорт CSV и healthcheck.

## Качество кода

В `pyproject.toml` добавлены настройки для ruff, black и mypy.

```bash
ruff check .
black .
mypy app
```

## Несколько решений по реализации

- **PostgreSQL как основная база.** В API возвращаются данные из PostgreSQL,
  потому что там хранится полная версия документа.
- **Elasticsearch только для поиска.** В индекс не дублируются все поля, там
  лежат только `id` и `text`.
- **Результаты сортируются по дате из БД.** Это требование задания, поэтому
  после поиска по индексу сервис загружает документы и сортирует их по
  `created_date`.
- **CLI-команды вместо лишних endpoint'ов.** Импорт, переиндексация и проверка
  консистентности относятся скорее к обслуживанию сервиса, поэтому вынесены в
  `app.cli`.
- **Без сложной очереди синхронизации.** Для тестового задания достаточно
  прямой записи в БД и индекс. В реальном проекте здесь можно было бы добавить
  outbox или очередь.

## Обработка ошибок

- пустой поисковый запрос возвращает ошибку;
- `limit` не может быть больше 20;
- удаление несуществующего документа возвращает `404`;
- если id найден в Elasticsearch, но документа уже нет в PostgreSQL, сервис
  пропускает такой id и пишет сообщение в лог;
- если документ есть в PostgreSQL, но уже отсутствует в Elasticsearch, удаление
  все равно считается успешным;
- если Elasticsearch недоступен во время поиска или удаления, API возвращает
  `503`.

## Что можно улучшить позже

- Добавить интеграционные тесты с реальными PostgreSQL и Elasticsearch.
- Добавить retry для временных ошибок Elasticsearch.
- Сделать outbox или очередь для более надежной синхронизации БД и индекса.
- Добавить пагинацию, если понадобится выдавать больше 20 результатов.
- Настроить analyzer Elasticsearch на реальном наборе данных.
- Добавить CI с тестами, линтером и проверкой типов.

## Примечание

Проект сделан как тестовое задание. Я держал фокус на простоте, читаемости и
запуске одной командой через Docker Compose.
