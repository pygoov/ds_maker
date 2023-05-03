import argparse

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from openai_client import OpenAIClient

parser = argparse.ArgumentParser()
parser.add_argument("tg_token", help="Telegram token")
parser.add_argument("open_ai_token", help="OpenAI token")
args = parser.parse_args()


bot = Bot(token=args.tg_token)
oai_client = OpenAIClient(args.open_ai_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Приветствую!")


@dp.message_handler(content_type=ContentType.TEXT)
async def message_handler(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
