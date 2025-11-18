from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()


dialog = Dialog(
    Window(
        Const(
            "Привет! Я помогу с генерацией текста по запросу.\n"
            "Отправьте сообщение — я отвечу с учётом контекста.\n\n"
            "Нажмите ‘Новый запрос’, чтобы сбросить контекст."
        ),
        Button(Const("Новый запрос"), id="new_request"),
        state=MainSG.main,
    )
)

