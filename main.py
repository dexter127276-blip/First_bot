import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from gigachat_client import GigaChatClient
from supabase_client import SupabaseClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GIGACHAT_API_URL = os.getenv("GIGACHAT_API_URL")
GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

if not TG_BOT_TOKEN:
    raise RuntimeError("TG_BOT_TOKEN is not set in environment")

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
gigachat = GigaChatClient(GIGACHAT_API_URL, GIGACHAT_API_KEY)


def get_sample_market_data() -> dict:
    return {
        "summary": (
            "Индексы S&P 500 и NASDAQ немного выросли после отчетов компаний, "
            "финансовый сектор показывает стабильность, а акции технологий остаются в центре внимания."
        ),
        "indices": "S&P 500 +0.5%, NASDAQ +0.8%, Dow Jones +0.3%",
        "sectors": "технологии, финансы, здравоохранение",
        "trend": "рост на фоне позитивной отчетности и ожиданий снижения ставок",
    }


def get_sample_news() -> list[dict]:
    return [
        {
            "title": "Отчет Apple превзошел ожидания",
            "summary": "Продажи iPhone и сервисов помогли компании показать сильные квартальные результаты.",
        },
        {
            "title": "Центробанк обсуждает снижение ставки",
            "summary": "Рынок ожидает осторожные комментарии, которые могут поддержать акции банков.",
        },
        {
            "title": "Нефтяные цены стабилизировались",
            "summary": "Стоимость Brent остается близкой к $80 за баррель на фоне спроса и сокращения запасов.",
        },
    ]


def build_help_text() -> str:
    return (
        "Я инвестиционный бот для обзорных запросов по рынку.\n"
        "Доступные команды:\n"
        "/start — приветствие и инструкции\n"
        "/help — показать команды\n"
        "/market — обзор рынка\n"
        "/news — свежие финансовые новости\n"
        "/reset — очистить текущее состояние"
    )


def log_user(message: Message) -> None:
    supabase.create_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )


def log_interaction(message: Message, bot_response: str, request_type: str) -> None:
    supabase.log_request(
        telegram_id=message.from_user.id,
        request_type=request_type,
        command=message.text or "",
        prompt=bot_response[:1024],
    )
    supabase.log_history(
        telegram_id=message.from_user.id,
        user_message=message.text or "",
        bot_response=bot_response,
    )


@dp.message(Command("start"))
async def handle_start(message: Message) -> None:
    log_user(message)
    text = (
        "Привет! Я бот для инвестора, который помогает быстро получать обзор рынка и новости.\n"
        "Попробуй команду /market для обзора и /news для новостей."
    )
    await message.answer(text)


@dp.message(Command("help"))
async def handle_help(message: Message) -> None:
    log_user(message)
    await message.answer(build_help_text())


@dp.message(Command("market"))
async def handle_market(message: Message) -> None:
    log_user(message)
    market_data = get_sample_market_data()
    overview = gigachat.generate_market_overview(market_data)
    response = f"*Обзор рынка*\n\n{overview}"
    await message.answer(response, parse_mode="Markdown")
    log_interaction(message, overview, request_type="market")


@dp.message(Command("news"))
async def handle_news(message: Message) -> None:
    log_user(message)
    news_items = get_sample_news()
    summary = gigachat.summarize_news(news_items)
    response = f"*Свежие новости рынка*\n\n{summary}"
    await message.answer(response, parse_mode="Markdown")
    log_interaction(message, summary, request_type="news")


@dp.message(Command("reset"))
async def handle_reset(message: Message) -> None:
    log_user(message)
    text = "Готово. Если хочешь, спроси обзор рынка или новости снова." 
    await message.answer(text)


@dp.message()
async def handle_unknown(message: Message) -> None:
    await message.answer(
        "Я понимаю команды /market и /news. Напиши /help, чтобы увидеть все доступные команды."
    )


async def main() -> None:
    try:
        logger.info("Запуск Telegram-бота...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
