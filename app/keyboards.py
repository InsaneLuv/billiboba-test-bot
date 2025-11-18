from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="♻️ Новый запрос"), KeyboardButton(text="🆘 Помощь")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Напишите сообщение",
    )

