from pyrogram import Client
from pytgcalls import PyTgCalls
from configs import config


user = Client(config.SESSION, config.API_ID, config.API_HASH)


bot = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins={"root": "plugins"},
)

call_py = PyTgCalls(user)
