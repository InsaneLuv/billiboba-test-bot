from __future__ import annotations

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka, inject

from app.keyboards import main_reply_keyboard
from app.services.chatgpt import ChatService


router = Router(name=__name__)


@router.message(F.text)
@inject
async def handle_text(message: Message, chat: FromDishka[ChatService]):
    text = message.text or ""

    if "♻️" in text.strip().lower():
        await chat.clear_history(user_id=message.from_user.id)
        await message.answer("Контекст очищен.", reply_markup=main_reply_keyboard())
        return

    if "🆘" in text.strip().lower():
        await message.answer(
            "Отправьте текст и я отвечу!\n"
            "Кнопка 'Новый запрос' сбросит историюб диалога.",
            reply_markup=main_reply_keyboard(),
        )
        return

    try:
        reply = await chat.generate_reply(user_id=message.from_user.id, text=text)
    except Exception as e:
        await message.answer("Не удалось обработать ваше сообщение. Попробуйте позже.")
        return

    await message.answer(reply, reply_markup=main_reply_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)

