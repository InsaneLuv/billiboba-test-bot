from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from app.config import get_settings, Settings
from app.di import AppProvider
from app.dialogs.main_dialog import dialog
from app.handlers import callbacks as callbacks_handlers, commands as commands_handlers, messages as messages_handlers
from app.services.chatgpt import ChatService


async def on_startup(_: Dispatcher, chat: ChatService):
    await chat.ensure_indexes()


async def main() -> None:
    settings: Settings = get_settings()

    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    container = make_async_container(AppProvider())
    setup_dishka(container=container, router=dp)

    dp.include_router(commands_handlers.router)
    dp.include_router(messages_handlers.router)
    dp.include_router(callbacks_handlers.router)

    dp.include_router(dialog)
    setup_dialogs(dp)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="🚀"),
            BotCommand(command="help", description="🆘"),
        ]
    )

    chat: ChatService = await container.get(ChatService)
    await on_startup(dp, chat)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
