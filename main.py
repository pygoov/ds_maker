import argparse

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, ParseMode
from typing import List

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

HELP_MSG = (
    "Пожалуйста, напишите мне две строки в сообщении.\n"
    "В первой строке описание класса.\n"
    "Во второй строке, пример вопроса который яперефразурую.\n\n"
    "пример сообщений:\n\n"
    "льготный возраст ребёнка, для заселения без платы\n"
    "сколько лет ребёнку должно быть, чтобы нас бесплатно заселили?\n"
)


async def make_new_line(class_line: str,
                        text_line: str,
                        temperature: float,
                        presence_penalty: float,
                        n: int) -> List[str]:
    p = (
        PROMPT
        .replace("<CLASS>", class_line)
        .replace("<TEXT>", text_line)
    )    
    result = await oai_client.completions(
        prompt=p,
        temperature=temperature,
        presence_penalty=presence_penalty,
        max_tokens=500,
        n=n,
        stop="\n"
    )
    return [x["text"] for x in result if "text" in x]


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(HELP_MSG)


@dp.message_handler(content_types=ContentType.TEXT)
async def message_handler(message: types.Message):
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

    print(f"run genegate - {message.from_user}")
    print(f'{class_line=}')
    print(f'{text_line=}')

    for temperature in [0.25, 0.75, 1, 1.25]:
        for presence_penalty in [-0.5, 0, 0.5]:
            try:
                line = (await make_new_line(
                    class_line,
                    text_line,
                    temperature,
                    presence_penalty,
                    1
                ))[0]
                # await message.answer(line)
                await message.answer(
                    f'=== [t:{temperature}|p:{presence_penalty}] ===\n{line}'
                )
            except Exception as e:
                print(e)
            # line = "\n".join(lines)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
