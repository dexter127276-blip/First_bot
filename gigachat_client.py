import logging
import requests

logger = logging.getLogger(__name__)

class GigaChatClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def _send_prompt(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "giga-chat-1",
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 400,
        }

        try:
            response = requests.post(self.api_url, json=body, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Поддержка стандартного ответа в стиле chat completion
            return data.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
        except Exception as exc:
            logger.warning("GigaChat request failed: %s", exc)
            return ""

    def generate_market_overview(self, market_data: dict) -> str:
        prompt = (
            "Ты инвестиционный помощник. "
            "Сделай краткий обзор фондового рынка на основе данных ниже. "
            "Выдели важные факты и обрати внимание на ситуацию с индексами и основными секторами.\n\n"
            f"{market_data['summary']}"
        )
        answer = self._send_prompt(prompt)
        if answer:
            return answer.strip()
        return self._fallback_market_text(market_data)

    def summarize_news(self, news_items: list[dict]) -> str:
        formatted = "\n".join([f"- {item['title']}: {item['summary']}" for item in news_items])
        prompt = (
            "Ты инвестиционный помощник. "
            "Сделай краткий обзор новостей и выдели самые важные события для фондового рынка.\n\n"
            f"Новости:\n{formatted}"
        )
        answer = self._send_prompt(prompt)
        if answer:
            return answer.strip()
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
