from typing import Iterable
from pytgcalls import PyTgCalls
from configs import config
from pyrogram import Client as RawClient
from pyrogram.storage import Storage


class Client(RawClient):
    def __init__(
        self,
        session_name: str | Storage,
        api_id: int | str,
        api_hash: str,
        bot_token: str = None,
        plugins: dict[str, str] = None,
    ):
        super().__init__(
            session_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins=plugins,
        )

    async def get_username(self):
        return (await self.get_me()).username

    async def get_full_name(self):
        me = await self.get_me()
        return f"{me.first_name} {me.last_name or ''}"

    async def mention(self, user_ids: Iterable[int | str] | str | int):
        return (await self.get_users(user_ids)).mention


user = Client(config.session, config.api_id, config.api_hash)
bot = Client(
    ":memory:",
    config.api_id,
    config.api_hash,
    bot_token=config.bot_token,
    plugins={"root": "solidmusic.plugins"},
)
user.__class__.__module__ = "pyrogram.client"
call_py = PyTgCalls(user)
