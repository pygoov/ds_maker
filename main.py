import argparse

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from openai_client import OpenAIClient

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tg_token", help="Telegram token")
parser.add_argument("-o", "--open_ai_token", help="OpenAI token")
args = parser.parse_args()

bot = Bot(token=args.tg_token)
oai_client = OpenAIClient(args.open_ai_token)
dp = Dispatcher(bot)

with open("./prompt.txt", "r", encoding="utf-8") as f:
    PROMPT = f.read()


async def make_new_line(class_line: str, text_line: str) -> str:
    p = (
        PROMPT
        .replace("<CLASS>", class_line)
        .replace("<TEXT>", text_line)
    )
    result = await oai_client.completions(
        prompt=p,
        temperature=1.2,
        presence_penalty=0.5,
        max_tokens=500,
        stop="\n"
    )
    return result


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Приветствую!")


@dp.message_handler(content_types=ContentType.TEXT)
async def message_handler(message: types.Message):
    text = message.text
    sp = text.split("\n")
    if len(sp) != 2:
        await message.answer(
            "Пожалуйста, напишите мне две строки в сообщении.\n"
            "В первой строке описание класса.\n"
            "Во второй строке, пример вопроса который яперефразурую.\n\n"
            "пример сообщений:\n"
            "```\n"
            "получение паспорта\n"
            "как получить паспорт?\n"
            "```"
        )
        return

    class_line = sp[0].strip()
    text_line = sp[1].strip()

    if not class_line or not text_line:
        await message.answer(
            "Пожалуйста, напишите мне две строки в сообщении.\n"
            "В первой строке описание класса.\n"
            "Во второй строке, пример вопроса который яперефразурую.\n\n"
            "пример сообщений:\n"
            "```\n"
            "получение паспорта\n"
            "как получить паспорт?\n"
            "```"
        )
        return

    line = await make_new_line(class_line, text_line)
    await message.answer(line)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
