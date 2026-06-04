import logging
from supabase import create_client

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)

    def create_or_update_user(self, telegram_id: int, username: str | None, first_name: str | None) -> None:
        payload = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
        }
        try:
            self.client.table("users").upsert(payload, on_conflict="telegram_id").execute()
        except Exception as exc:
            logger.warning("Supabase create_or_update_user failed: %s", exc)

    def log_request(self, telegram_id: int, request_type: str, command: str, prompt: str | None) -> None:
        payload = {
            "telegram_id": telegram_id,
            "request_type": request_type,
            "command": command,
            "prompt": prompt,
        }
        try:
            self.client.table("requests").insert(payload).execute()
        except Exception as exc:
            logger.warning("Supabase log_request failed: %s", exc)

    def log_history(self, telegram_id: int, user_message: str, bot_response: str) -> None:
        payload = {
            "telegram_id": telegram_id,
            "user_message": user_message,
            "bot_response": bot_response,
        }
        try:
            self.client.table("history").insert(payload).execute()
        except Exception as exc:
            logger.warning("Supabase log_history failed: %s", exc)
