from aiogram import F, Router
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import FromDishka, inject

from app.services.chatgpt import ChatService


router = Router(name=__name__)


@router.callback_query(F.data.contains("new_request"))
@inject
async def new_request_clicked(call: CallbackQuery, chat: FromDishka[ChatService]):
    if call.from_user is None:
        await call.answer()
        return
    await chat.clear_history(user_id=call.from_user.id)
    await call.answer("Контекст очищен", show_alert=False)
    await call.message.answer("Контекст диалога сброшен. Введите новый запрос.")

