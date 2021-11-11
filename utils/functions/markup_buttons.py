from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dB.lang_utils import get_message as gm
from configs import config


def start_markup(chid: int, bot_username: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    gm(chid, "add_to_chat"),
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    gm(chid, "helpbutton"), callback_data="cbhelp"
                ),
                InlineKeyboardButton(
                    gm(chid, "maintainer"), url="https://t.me/talktoabdul_bot"
                ),
            ],
            [
                InlineKeyboardButton(
                    gm(chid, "channel"), url=config.CHANNEL
                ),
                InlineKeyboardButton(
                    gm(chid, "group_support"), url=config.SUPPORT
                ),
            ],
            [
                InlineKeyboardButton(
                    gm(chid, "source_code"),
                    url="https://github.com/DoellBarr/solidmusic",
                )
            ],
        ]
    )
