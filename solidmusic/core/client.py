from typing import Any, Iterable, Optional

from configs import config
from pyrogram import Client as RawClient
from pyrogram.types import User
from pytgcalls import PyTgCalls


class Client(RawClient):
    def __init__(self, **kwargs: Any):
        self._me: Optional[User] = None
        super().__init__(**kwargs)

    async def get_me(self, cached: bool = True) -> User:
        if not cached or self._me is None:
            self._me = await super().get_me()

        return self._me

    async def start(self):
        await super().start()
        self._me = await self.get_me()

    async def get_username(self) -> Optional[str]:
        return (await self.get_me()).username

    async def get_full_name(self) -> str:
        me = await self.get_me()
        return f"{me.first_name} {me.last_name or ''}"

    async def mention(self, user_ids: Iterable[int | str] | str | int) -> str:
        return (await super().get_users(user_ids)).mention


bot = Client(
    session_name="solidmusic-bot",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token,
    plugins={"root": "solidmusic.plugins"},
)

user = Client(
    session_name=config.session,
    api_id=config.api_id,
    api_hash=config.api_hash,
)
user.__class__.__module__ = "pyrogram.client"

call_py = PyTgCalls(user)
