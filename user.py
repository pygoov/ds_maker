import asyncio
import random
import keyboards as kb

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ParseMode
from typing import List, Dict, Optional


from generator import Generator


GENERATION_POOL_SIZE = 4


class User:
    class_line: Optional[str]
    text_line: Optional[str]
    last_line: Optional[str]
    save_lines: List[str]
    generation_pool: asyncio.Queue[str]

    def __init__(self,
                 user: types.User,
                 generator: Generator
                 ) -> None:
        self.user = user
        self.bot = user.bot
        self.generator = generator
        self.generation_pool = asyncio.Queue()

        self.clear()

        self.task = asyncio.create_task(self._main_loop())

    @property
    def chat_id(self) -> int:
        return self.user.id

    @property
    def is_empty(self) -> bool:
        return not (
            bool(self.class_line) and
            bool(self.text_line) and
            bool(self.last_line)
        )

    def __str__(self) -> str:
        return f'User<{self.user.full_name}|{self.user.id}>'

    def clear(self) -> None:
        self.class_line = None
        self.text_line = None
        self.last_line = None
        self.save_lines = []

    def save_line(self):
        if self.last_line is None:
            raise Exception(f"[{self}] last_line is None")
        self.save_lines.append(self.last_line)

    async def _main_loop(self) -> None:
        print(f"[{self}] start _main_loop")
        while True:
            if (
                (self.generation_pool.qsize() >= GENERATION_POOL_SIZE) or
                not (self.class_line or self.text_line)
            ):
                await asyncio.sleep(1)
                continue

            if self.class_line is None:
                raise Exception(f"[{self}] class_line is None")
            if self.text_line is None:
                raise Exception(f"[{self}] text_line is None")
            temperature = 0.25 + (random.random() * 0.5)
            presence_penalty = random.random() - 0.5
            try:
                line = await self.generator.make_new_line(
                    self.class_line,
                    self.text_line,
                    temperature,
                    presence_penalty,
                )
                line = line.strip()
                self.generation_pool.put_nowait(line)
            except Exception as e:
                print(f'error in generation[{type(e)}]: {e}')

            await asyncio.sleep(1)

    async def make_line(self) -> str:
        line = await self.generation_pool.get()
        self.last_line = line
        return line

    async def safe_generate(self, message: types.Message) -> None:
        await message.edit_text("♻️ генерирую ♻️")
        try:
            line = await self.make_line()
            line = (
                f'Строка: `{line}`'
                f'\n\nсохранено строк: `{len(self.save_lines)}`'
            )
            await message.edit_text(
                line,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=kb.LINE_KB,
            )
        except Exception as e:
            print(f'Error [{type(e)}]{e}')
            await message.edit_text(
                "⚠️ простите, при генерации чтото пошло не так ⚠️"
            )


class UserMiddleware(BaseMiddleware):
    def __init__(self,
                 users: Dict[int, User],
                 generator: Generator):
        self.users = users
        self.generator = generator
        super().__init__()

    async def _get_user(self, from_user: types.User) -> User:
        user_id = from_user.id
        user = self.users.get(user_id, None)
        if user is None:
            user = User(from_user, self.generator)
            self.users[user_id] = user
        return user

    async def on_process_callback_query(self,
                                        query: types.CallbackQuery,
                                        data: dict):
        user = await self._get_user(query.from_user)
        data["user"] = user

        print(f'{user} send callback.data: "{query.data}"')

    async def on_process_message(self, message: types.Message, data: dict):
        user = await self._get_user(message.from_user)
        data["user"] = user

        text_type = "command" if message.is_command() else "text"
        print(f'{user} send {text_type}: "{message.text}"')
