# TeamFinder (вариант 2)

Проект выполнен на Django 5.2 + PostgreSQL.
Реализован вариант 2: навыки пользователей и фильтрация участников по навыкам.

## Быстрый старт для ревьюера

### 1. Требования

- Python 3.10+
- Docker + Docker Compose

### 2. Установка зависимостей

В корне проекта:

```bash
python -m venv venv
```

Активация окружения:

- Windows PowerShell:
  ```bash
  venv\Scripts\Activate.ps1
  ```
- Windows Git Bash:
  ```bash
  source venv/Scripts/activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

Установка пакетов:

```bash
pip install -r requirements.txt
```

### 3. Настройка `.env`

Скопировать шаблон:

- Linux/Mac/Git Bash:
  ```bash
  cp .env_example .env
  ```
- Windows PowerShell:
  ```bash
  Copy-Item .env_example .env
  ```

Проверить значения в `.env`:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=2
```

### 4. Запуск PostgreSQL

```bash
docker compose up -d
```

### 5. Миграции и запуск сервера

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Проект будет доступен:

- http://127.0.0.1:8000/projects/list/
- http://127.0.0.1:8000/admin/

## Что проверить по функционалу

### Базовая часть

- Регистрация/вход/выход пользователя.
- Редактирование профиля и смена пароля.
- Список проектов, создание и редактирование проекта.
- Завершение проекта владельцем (`status=open -> closed`).
- Присоединение/выход из проекта для авторизованных пользователей.
- Список пользователей `/users/list/` с пагинацией.

### Вариант 2

- На странице пользователя есть блок навыков.
- Владелец профиля добавляет/удаляет навыки без перезагрузки.
- Работает автодополнение навыков.
- Можно создать новый навык из интерфейса.
- На `/users/list/?skill=<Навык>` фильтрация оставляет только пользователей с выбранным навыком.
- Активный фильтр подсвечивается, есть сброс фильтра.

## Реализованные особенности

- Кастомная модель пользователя с логином по email (`AUTH_USER_MODEL`).
- Валидация телефона: `8XXXXXXXXXX` или `+7XXXXXXXXXX`, с проверкой уникальности.
- Валидация GitHub-ссылок: только домен `github.com`.
- Шаблоны подключаются через `TASK_VERSION=2` (`templates_var2`).

## Остановка сервисов

```bash
docker compose down
```
