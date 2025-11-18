from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from app.dialogs.main_dialog import MainSG
from app.keyboards import main_reply_keyboard
from app.services.chatgpt import ChatService


router = Router(name=__name__)


@router.message(CommandStart())
@inject
async def cmd_start(
    message: Message,
    dialog_manager: DialogManager,
    chat: FromDishka[ChatService],
):
    await chat.clear_history(user_id=message.from_user.id)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать диалог сначала\n"
        "/help - Помощь\n\n"
        "Отправьте любое текстовое сообщение - я постараюсь ответить.\n"
        "Кнопка 'Новый запрос' тоже начинает диалог сначала.",
        reply_markup=main_reply_keyboard(),
    )

