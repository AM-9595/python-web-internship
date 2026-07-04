

REST API для управления командами, проектами, задачами и комментариями.

## Возможности

- Регистрация пользователей и JWT-аутентификация.
- CRUD для:
  - Команд
  - Проектов
  - Задач
  - Комментариев
- Разграничение прав доступа:
  - Только участники команды могут просматривать проекты.
  - Только владелец команды может добавлять участников.
- Бизнес-правила:
  - Нельзя изменить статус задачи с done обратно на new.
- Логирование основных действий.
- Покрытие проекта модульными тестами (10+ тестов).

---

## Технологический стек

- Python 3.11
- Django 4+
- Django REST Framework
- PostgreSQL (SQLite для разработки)
- JWT Authentication
- Docker
- Docker Compose

---

# Запуск проекта

## Локальный запуск

### 1. Клонировать репозиторий
git clone <repository_url>
cd team-tasks-api

### 2. Создать виртуальное окружение

Linux / macOS
python -m venv .venv
source .venv/bin/activate

Windows
.venv\Scripts\activate

### 3. Установить зависимости
pip install -r requirements.txt

### 4. Выполнить миграции
python manage.py makemigrations
python manage.py migrate

### 5. Создать суперпользователя
python manage.py createsuperuser

### 6. Запустить сервер
python manage.py runserver

API будет доступно по адресу:
http://127.0.0.1:8000/api/

---

# Запуск через Docker

### Собрать и запустить контейнеры
docker-compose up --build

### Выполнить миграции
docker-compose exec web python manage.py migrate

### Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

После запуска API доступно по адресу:
http://localhost:8000/api/

---

# API Endpoints

## Аутентификация

| Метод | Endpoint | Описание |
|--------|----------|----------|
| POST | /api/register/ | Регистрация пользователя |
| POST | /api/token/ | Получение JWT-токена |
| POST | /api/token/refresh/ | Обновление токена |

---

## Команды

| Метод | Endpoint | Описание |
|--------|----------|----------|
| GET | /api/teams/ | Список своих команд |
| POST | /api/teams/ | Создание команды |
| GET | /api/teams/{id}/ | Просмотр команды |
| POST | /api/teams/{id}/add-member/ | Добавление участника |

---

## Проекты

| Метод | Endpoint | Описание |
|--------|----------|----------|
| GET | /api/projects/ | Список проектов |
| POST | /api/projects/ | Создание проекта |
| GET | /api/projects/{id}/ | Просмотр проекта |

---

## Задачи

| Метод | Endpoint | Описание |
|--------|----------|----------|
| GET | /api/tasks/ | Список задач |
| POST | /api/tasks/ | Создание задачи |
| GET | /api/tasks/{id}/ | Просмотр задачи |
| PATCH | /api/tasks/{id}/ | Обновление задачи |
| DELETE | /api/tasks/{id}/ | Удаление задачи |

---

## Комментарии

| Метод | Endpoint | Описание |
|--------|----------|----------|
| GET | /api/comments/ | Список комментариев |
| POST | /api/comments/ | Создание комментария |
| GET | /api/comments/{id}/ | Просмотр комментария |
| DELETE | /api/comments/{id}/ | Удаление комментария |

---

## Аутентификация

Все эндпоинты, кроме:

- /api/register/
- /api/token/
- /api/token/refresh/

требуют JWT-аутентификации.

Необходимо передавать заголовок:
Authorization: Bearer <access_token>

---

# Примеры запросов

## Регистрация
POST /api/register/
Content-Type: application/json
{
    "username": "john",
    "password": "secret123",
    "email": "john@example.com"
}

---

## Получение JWT
POST /api/token/
Content-Type: application/json
{
    "username": "john",
    "password": "secret123"
}

Ответ:
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}

---

## Создание команды
POST /api/teams/
Authorization: Bearer <access_token>
Content-Type: application/json
{
    "name": "Разработчики"
}

---

## Добавление участника
POST /api/teams/1/add-member/
Authorization: Bearer <access_token>
Content-Type: application/json
{
    "user_id": 2
}

---

## Создание задачи
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json
{
    "title": "Реализовать логин",
    "project": 1,
    "assigned_to": 2
}

---

## Изменение статуса задачи
PATCH /api/tasks/1/
[04.07.2026 22:49] M7R95: Authorization: Bearer <access_token>
Content-Type: application/json
{
    "status": "done"
}

---

# Тестирование

Запуск всех тестов:
pytest

или
python manage.py test api

---

# Логирование

Приложение ведёт журнал основных действий.

Логи:

- записываются в файл app.log;
- выводятся в консоль.

Настройка логирования производится в settings.py.

---

# Лицензия

Проект создан в учебных целях.