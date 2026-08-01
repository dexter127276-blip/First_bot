import logging

from gigachat import GigaChat
from gigachat.exceptions import GigaChatException

logger = logging.getLogger(__name__)


class GigaChatClient:
    async def _send_prompt(self, prompt: str) -> str:
        try:
            async with GigaChat() as client:
                response = await client.achat.create(prompt)

            if not response.messages:
                return ""

            content = response.messages[0].content
            if isinstance(content, str):
                return content.strip()

            return "".join(
                part.text
                for part in content or []
                if getattr(part, "text", None)
            ).strip()
        except GigaChatException as exc:
            logger.warning("GigaChat request failed: %s", exc)
            return ""
        except Exception:
            logger.exception("Unexpected GigaChat client error")
            return ""

    async def generate_market_overview(self, market_data: dict) -> str:
        prompt = (
            "Ты инвестиционный помощник. "
            "Сделай краткий обзор фондового рынка на основе данных ниже. "
            "Выдели важные факты и обрати внимание на ситуацию с индексами и основными секторами. "
            "Не добавляй факты, которых нет в исходных данных.\n\n"
            f"Сводка: {market_data['summary']}\n"
            f"Индексы: {market_data['indices']}\n"
            f"Секторы: {market_data['sectors']}\n"
            f"Тренд: {market_data['trend']}"
        )
        answer = await self._send_prompt(prompt)
        if answer:
            return answer
        return self._fallback_market_text(market_data)

    async def summarize_news(self, news_items: list[dict]) -> str:
        formatted = "\n".join([f"- {item['title']}: {item['summary']}" for item in news_items])
        prompt = (
            "Ты инвестиционный помощник. "
            "Сделай краткий обзор новостей и выдели самые важные события для фондового рынка. "
            "Не добавляй факты, которых нет в исходных новостях.\n\n"
            f"Новости:\n{formatted}"
        )
        answer = await self._send_prompt(prompt)
        if answer:
            return answer
        return self._fallback_news_text(news_items)

    def _fallback_market_text(self, market_data: dict) -> str:
        return (
            "Обзор рынка:\n"
            f"Главные индексы: {market_data['indices']}.\n"
            f"Лучшие сектора: {market_data['sectors']}.\n"
            f"Ключевой тренд: {market_data['trend']}."
        )

    def _fallback_news_text(self, news_items: list[dict]) -> str:
        lines = [f"{item['title']}: {item['summary']}" for item in news_items]
        return "Новости:\n" + "\n".join(lines)
