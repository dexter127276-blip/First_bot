# Market Mentor Telegram Bot

Простой учебный бот для инвестора на фондовом рынке.

## Что делает бот

- `/market` — показывает обзор рынка
- `/news` — показывает свежие финансовые новости
- `/start` — приветствие
- `/help` — список команд
- `/reset` — очистка сессии

## Стек

- Python 3.13
- aiogram 3.0
- официальный Python SDK GigaChat
- Supabase
- python-dotenv

## Установка

1. Скопируй `.env.example` в `.env`.
2. Заполни переменные окружения:
   - `TG_BOT_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GIGACHAT_CREDENTIALS`
   - `GIGACHAT_SCOPE`
   - `GIGACHAT_BASE_URL`
   - `GIGACHAT_MODEL`
   - `GIGACHAT_CA_BUNDLE_FILE`
3. Установи зависимости:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Запусти бота:
   ```bash
   python main.py
   ```

## База данных Supabase

В Supabase используются таблицы:
- `users`
- `requests`
- `history`

Если таблицы не созданы, выполни миграцию
`supabase/migrations/20260604203000_create_bot_tables.sql`
в Supabase SQL Editor.


