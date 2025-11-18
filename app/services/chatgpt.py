from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from openai import OpenAI
from pymongo.asynchronous.collection import AsyncCollection

from app.config import Settings


class ChatService:
    def __init__(
        self,
        client: OpenAI,
        collection: AsyncCollection,
        settings: Settings,
    ) -> None:
        self.client = client
        self.collection = collection
        self.settings = settings

    async def ensure_indexes(self) -> None:
        await self.collection.create_index([("user_id", 1), ("created_at", 1)])

    async def clear_history(self, user_id: int) -> None:
        await self.collection.delete_many({"user_id": user_id})

    async def _fetch_history(self, user_id: int) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", 1)
        docs = await cursor.to_list(length=self.settings.max_history_messages)
        messages: List[Dict[str, str]] = [
            {"role": d["role"], "content": d["content"]} for d in docs
        ]
        return messages[-self.settings.max_history_messages :]

    async def generate_reply(self, user_id: int, text: str) -> str:
        now = datetime.now(timezone.utc)
        await self.collection.insert_one(
            {
                "user_id": user_id,
                "role": "user",
                "content": text,
                "created_at": now,
            }
        )

        history = await self._fetch_history(user_id)
        messages = [{"role": "system", "content": self.settings.system_prompt}] + history

        completion = self.client.chat.completions.create(
            model=self.settings.openai_model,
            messages=messages,
        )
        reply = completion.choices[0].message.content or ""

        await self.collection.insert_one(
            {
                "user_id": user_id,
                "role": "assistant",
                "content": reply,
                "created_at": datetime.now(timezone.utc),
            }
        )
        return reply

