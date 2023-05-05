import argparse

import keyboards as kb

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, ParseMode

from typing import Dict

from openai_client import OpenAIClient
from generator import Generator
from user import User, UserMiddleware


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tg_token", help="Telegram token")
parser.add_argument("-o", "--open_ai_token", help="OpenAI token")
args = parser.parse_args()

bot = Bot(token=args.tg_token)
oai_client = OpenAIClient(args.open_ai_token)
generator = Generator(oai_client)
dp = Dispatcher(bot)
users: Dict[int, User] = {}


HELP_MSG = (
    "Пожалуйста, напишите мне две строки в сообщении.\n"
    "В первой строке описание класса.\n"
    "Во второй строке, пример вопроса который яперефразурую.\n\n"
    "пример сообщений:\n\n"
    "льготный возраст ребёнка, для заселения без платы\n"
    "сколько лет ребёнку должно быть, чтобы нас бесплатно заселили?\n"
)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, user: User):
    user.clear()
    await message.answer(HELP_MSG)


@dp.message_handler(content_types=ContentType.TEXT)
async def message_handler(message: types.Message, user: User):
    text = message.text
    sp = text.split("\n")
    if len(sp) != 2:
        await message.answer(HELP_MSG)
        return

    class_line = sp[0].strip()
    text_line = sp[1].strip()

    if not class_line or not text_line:
        await message.answer(HELP_MSG)
        return

    print(f'{class_line=}')
    print(f'{text_line=}')

    user.class_line = class_line
    user.text_line = text_line

    await message.answer(
        "Установлена новая цель для генерации.\n"
        f"Класс: `{class_line}`\n"
        f"Пример: `{text_line}`",
        parse_mode=ParseMode.MARKDOWN
    )
    await message.answer(
        "Начало генерации.\nОцените выданные предложения, а когда, "
        "накопится достаточное кол-во, наажмите сохранить для "
        "скачивания excel документа со списком."
    )
    msg = await message.answer("генерирую")
    await user.safe_generate(msg)


@dp.callback_query_handler(text="bnt_line_no")
async def bnt_line_no_handler(query: types.CallbackQuery, user: User):
    message = query.message
    if user.is_empty:
        await message.edit_text(
            "⚠️ строка устарела, необходимо заного задать цель генерации! ⚠️",
            reply_markup=None
        )
        await message.answer(HELP_MSG)
        return
    await user.safe_generate(message)


@dp.callback_query_handler(text="bnt_line_yes")
async def bnt_line_yes_handler(query: types.CallbackQuery, user: User):
    message = query.message
    if user.is_empty:
        await message.edit_text(
            "⚠️ строка устарела, необходимо заного задать цель генерации! ⚠️",
            reply_markup=None
        )
        await message.answer(HELP_MSG)
        return
    user.save_line()
    await user.safe_generate(message)


@dp.callback_query_handler(text="bnt_line_save")
async def bnt_line_save_handler(query: types.CallbackQuery, user: User):
    lines = user.save_lines
    await query.message.edit_text(
        (
            "⚙️ выгрузка данных ⚙️\n"
            f"сохранено строк: {len(lines)}"
        ),
        reply_markup=None
    )
    if not lines:
        await query.message.answer("невозможно выгрузить 0 строк")
        return

    text = "\n".join(lines)
    await query.message.answer(f"lines: {text}")


if __name__ == '__main__':
    dp.middleware.setup(UserMiddleware(users, generator))
    executor.start_polling(dp, skip_updates=True)
