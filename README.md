# TaskBot Project

Cистема управления задачами, состоящая из Django бэкенда и Telegram бота. Проект позволяет пользователям создавать напоминания через бота, которые обрабатываются в фоновом режиме через Celery и доставляются пользователю точно в срок.

## Основные функции
*   **Telegram Bot**: Интерфейс для взаимодействия с пользователем (создание, просмотр задачи).
*   **Django Backend**: Центральный узел управления данными, API для бота и панель администратора.
*   **Celery & Redis**: Система фоновых задач для обработки очередей и отправки уведомлений.
*   **PostgreSQL**: Хранение данных пользователей и их задач.

## Технологический стек
*   **Python 3.14**
*   **Django**
*   **Aiogram**
*   **Celery** 
*   **Redis**
*   **PostgreSQL**
*   **Docker & Docker Compose**

## Настройка окружения
Для запуска проекта необходимо создать файл `.env` в корневой директории и заполнить его следующими данными:

```.env
# Основные настройки Django
DJANGO_SECRET_KEY=your_django_secret_key
BACKEND_BASE_URL=http://django:8000

# Настройки Telegram бота
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
BOT_API_SECRET=your_api_secret_key

# Celery и Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# База данных PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

### Запуск на локальной машине
```bash
# Сборка и запуск всех сервисов (Django, Telegram bot, Celery, DB, Redis)
docker-compose up --build
```