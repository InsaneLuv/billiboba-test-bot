# billiboba-test-bot

Telegram‑бот на aiogram, интеграцией с OpenAI Chat Completions

## Возможности

- Диалог с LLM (OpenAI) с сохранением контекста переписки.
- Хранение истории сообщений в MongoDB, очистка истории по команде/кнопке.
- Приветственное окно и кнопки через aiogram-dialog. (если понадобится более расширенный функционал)
- Иньекция зависимостей с пом. Dishka.

## Требования

- Python 3.13
- MongoDB
- токен Telegram‑бот
- Ключ OpenAI API

## Установка

В проекте используется `pyproject.toml` и `uv.lock`.

### Вариант с uv

1. Установите [uv](https://github.com/astral-sh/uv).
2. Выполните:

```bash
uv sync
```

### Вариант с pip

1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости (на основе `pyproject.toml`):

```bash
pip install .
```

## Конфигурация

Создайте файл `.env` в корне проекта скопируя .env.example.

Внесите значения токенов:

- Значения `BOT_TOKEN`, `OPENAI_API_KEY`.

## Запуск

Через uv:

```bash
uv run python -m app.main
```

Через Python:

```bash
python -m app.main
```

Бот сам выставит команды `/start` и `/help` при запуске. После старта:

- Кнопка «Новый запрос» очищает контекст истории.
- Сообщения пользователя отправляются в OpenAI, ответы приходят с учетом системы и истории.

## Архитектура и файлы

- `app/main.py` — инициализация бота, роутеров, DI‑контейнера, запуск поллинга.
- `app/di.py` — провайдеры Dishka: настройки, OpenAI клиент, MongoDB клиент/БД/коллекция, `ChatService`.
- `app/services/chatgpt.py` — логика общения с OpenAI и сохранение/получение истории из MongoDB.
- `app/handlers/commands.py` — обработчики команд `/start`, `/help`.
- `app/handlers/messages.py` — обработка текстовых сообщений, очистка истории по кнопке/фразе, вызов `ChatService`.
- `app/handlers/callbacks.py` — обработка нажатий inline‑кнопок (например, «Новый запрос»).
- `app/dialogs/main_dialog.py` — приветственное окно и основной диалог (aiogram-dialog).
- `app/keyboards.py` — клавиатуры (reply).
- `app/config.py` — конфигурация из `.env`.

## Хранилище и история

- Коллекция задается переменной `HISTORY_COLLECTION`.
- Индекс создается при старте: по `user_id` и `created_at`.
- В истории хранятся пары сообщений (user/assistant); лимит регулируется `MAX_HISTORY_MESSAGES`.