Apache Log Aggregator

Приложение для сбора и анализа логов веб-сервера Apache. Позволяет парсить текстовые логи, сохранять их в БД и просматривать через веб-интерфейс с фильтрацией.

🛠 Стек технологий

Backend: Python 3.10+, FastAPI, SQLAlchemy.

Database: SQLite (по умолчанию) / PostgreSQL.

Frontend: HTML5, Bootstrap 5, JavaScript (AJAX/XHR).

📋 Требования

Установите необходимые библиотеки:

Bash

pip install fastapi uvicorn sqlalchemy pyyaml passlib python-multipart

🚀 Запуск приложения

Настройка: В файле config.yaml укажите путь к папке с логами.

Запуск сервера:

Bash

uvicorn main:app --reload

Доступ: Откройте в браузере http://127.0.0.1:8000

🕹 Инструкция по работе

Вход: Используйте логин admin и пароль admin123.

Парсинг: Нажмите кнопку "Распарсить файлы", чтобы загрузить данные из access.log в базу данных.

Поиск: Используйте поле "Ключевое слово" для фильтрации по URL или методам.

Консоль: Для просмотра через терминал запустите python console_view.py.

📂 Структура файлов

main.py — сервер и API.

parser.py — логика разбора логов (поддерживает запуск по Cron).

database.py — подключение к БД и модели данных.

config.yaml — настройки путей и масок файлов.

static/ — файлы фронтенда.