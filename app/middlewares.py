from __future__ import annotations

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 3.0) -> None:
        self.delay = delay
        self._last_message_at: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or event.from_user is None:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.monotonic()
        last = self._last_message_at.get(user_id, 0.0)

        if now - last < self.delay:
            wait_left = self.delay - (now - last)
            seconds_left = int(wait_left) + (0 if wait_left.is_integer() else 1)
            try:
                await event.answer(
                    f"Анти-флуд!!! Подождите {seconds_left} сек. перед следующим сообщением."
                )
            except Exception:
                pass
            return

        self._last_message_at[user_id] = now
        return await handler(event, data)

