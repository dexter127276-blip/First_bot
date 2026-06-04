# Market Mentor Telegram Bot

Простой учебный бот для инвестора на фондовом рынке.

## Что делает бот

- `/market` — показывает обзор рынка
- `/news` — показывает свежие финансовые новости
- `/start` — приветствие
- `/help` — список команд
- `/reset` — очистка сессии

## Стек

- Python
- aiogram 3.0
- GigaChat
- Supabase
- python-dotenv

## Установка

1. Скопируй `.env.example` в `.env`.
2. Заполни переменные окружения:
   - `TG_BOT_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GIGACHAT_API_URL`
   - `GIGACHAT_API_KEY`
3. Установи зависимости:
   ```bash
   pip install -r requirements.txt
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

Если таблицы не созданы, создай их вручную по структуре из `Agent.md`.


