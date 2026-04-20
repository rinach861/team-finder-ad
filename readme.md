# TeamFinder (вариант 2)

## О проекте

TeamFinder - веб-приложение для поиска команды в учебных и pet-проектах.
Пользователи создают карточки проектов, указывают статус и ссылку на репозиторий,
подключаются к чужим проектам и находят участников по навыкам.

Проект реализован в рамках итогового задания, вариант 2:
работа с навыками пользователей и фильтрация участников по выбранному навыку.

## Основной функционал

- регистрация, вход и выход пользователя;
- просмотр и редактирование профиля, смена пароля;
- автогенерация аватара при создании пользователя (если аватар не загружен);
- список участников с фильтром по навыку;
- добавление и удаление навыков в профиле;
- создание проекта;
- просмотр списка проектов и страницы проекта;
- редактирование проекта (только владельцем);
- завершение проекта (закрытие статуса);
- присоединение/выход из участников проекта.

## Стек технологий

- Python 3.10+
- Django 5.2
- PostgreSQL 16
- Pillow
- python-decouple
- Docker Compose (для локального PostgreSQL)

## Запуск проекта локально

### 1. Подготовка окружения

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

Установка зависимостей:

```bash
pip install -r requirements.txt
```

### 2. Настройка `.env`

Создайте файл `.env` из шаблона:

- Linux/Mac/Git Bash:
  ```bash
  cp .env_example .env
  ```
- Windows PowerShell:
  ```bash
  Copy-Item .env_example .env
  ```

Пример содержимого `.env`:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5436
```

Назначение переменных:

- `DJANGO_SECRET_KEY` - секретный ключ Django;
- `DJANGO_DEBUG` - режим отладки (`True`/`False`);
- `POSTGRES_DB` - имя базы данных;
- `POSTGRES_USER` - пользователь БД;
- `POSTGRES_PASSWORD` - пароль пользователя БД;
- `POSTGRES_HOST` - хост PostgreSQL;
- `POSTGRES_PORT` - порт PostgreSQL.

### 3. Запуск PostgreSQL в Docker

```bash
docker compose up -d
```

Контейнер БД публикуется на `5436:5432` для избежания конфликта
с локальной PostgreSQL на порту `5432`.

### 4. Миграции и запуск Django

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

После запуска:

- приложение: http://127.0.0.1:8000/projects/list/
- админка: http://127.0.0.1:8000/admin/

## Полезные команды

```bash
python manage.py check
python manage.py makemigrations --check
```

Остановка сервисов:

```bash
docker compose down
```

## Скриншоты

Скриншоты локальной проверки находятся в директории:

- `docs/screenshots/`

## Автор

- Меджидов Ринат
