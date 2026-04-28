# Контрольная работа №4

Решение заданий по FastAPI: миграции Alembic, пользовательская обработка ошибок, валидация входных данных и модульные тесты.

## Что реализовано

- `Product` на SQLAlchemy с миграциями Alembic.
- Начальная миграция создает таблицу `products` и добавляет две записи.
- Вторая миграция добавляет обязательное поле `description`.
- Пользовательские исключения и единый формат ответов об ошибках.
- Пользовательская обработка ошибок валидации Pydantic/FastAPI.
- Эндпоинты для пользователей с in-memory хранилищем.
- Синхронные и асинхронные тесты через `pytest`, `httpx.AsyncClient`, `ASGITransport` и `Faker`.

## Установка и запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

После запуска документация доступна по адресу:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Проверка основной функциональности

```powershell
pytest
```

Примеры ручной проверки:

- `GET /products` - список продуктов из базы данных.
- `GET /demo-errors/a` - пример пользовательской ошибки `CustomExceptionA`.
- `GET /demo-errors/b` - пример пользовательской ошибки `CustomExceptionB`.
- `POST /validate-user` - проверка JSON-полезной нагрузки пользователя.
- `POST /users`, `GET /users/{user_id}`, `DELETE /users/{user_id}` - CRUD-сценарии для in-memory пользователей.

Пример валидного тела для `POST /validate-user`:

```json
{
  "username": "student",
  "age": 20,
  "email": "student@example.com",
  "password": "password1",
  "phone": "+79990000000"
}
```

## Миграции

```powershell
alembic upgrade head
alembic current
alembic downgrade -1
```
