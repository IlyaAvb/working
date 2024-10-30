from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

markup_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Старт')]
    ],
    resize_keyboard=True
)

def create_change_button(state_name):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Изменить', callback_data=f'change_{state_name}')]
        ]
    )

done_markups = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text='Получить сумму', callback_data='get_sum')]
    ]
)

minus_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='МИНУС')]
    ],
    resize_keyboard=True
)