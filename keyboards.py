from typing import Union, List, Dict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_keyboard(data: List[Union[List[dict], dict]]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for button in data:
        if isinstance(button, dict):
            kb.add(
                InlineKeyboardButton(**button)
            )
        elif isinstance(button, list):
            kb.row(*[
                InlineKeyboardButton(**b)
                for b in button
            ])
    return kb


# LINE_KB = make_keyboard([
#     [
#         {
#             "text": "❌",
#             "callback_data": "bnt_line_no"
#         },
#         {
#             "text": "✅",
#             "callback_data": "bnt_line_yes"
#         }
#     ],
#     {
#         "text": "💾",
#         "callback_data": "bnt_line_save"
#     }
# ])

LINE_KB = make_keyboard([
    [
        {
            "text": "❌ пропустить",
            "callback_data": "bnt_line_no"
        },
        {
            "text": "✅ добавить",
            "callback_data": "bnt_line_yes"
        }
    ],
    {
        "text": "💾 сохранить и закончить",
        "callback_data": "bnt_line_save"
    }
])
