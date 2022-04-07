from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from configs import config
from solidmusic.database.lang_utils import gm
button = InlineKeyboardButton
markup = InlineKeyboardMarkup


def start_markup(chat_id: int, bot_username: str):
    return markup(
        [
            [
                button(
                    text=await gm(chat_id, "add_to_chat"),
                    url=f"https://t.me/{bot_username}?startgroup=true"
                )
            ],
            [
                button(
                    text=await gm(chat_id, "helpbutton"),
                    callback_data="cbhelp"
                ),
                button(
                    text=await gm(chat_id, "maintainer"),
                    url=f"tg://user?id={config.owner_id}"
                )
            ],
            [
                button(
                    text=await gm(chat_id, "source_code"),
                    url="https://github.com/DoellBarr/solidmusic"
                )
            ]
        ]
    )


def process_button(user_id: int, stream_type: str):
    numbers = ["1️⃣, 2️⃣, 3️⃣, 4️⃣, 5️⃣"]
    x = [
        button(
            f"{j}", callback_data=f"{stream_type} {count}|{user_id}"
        ) for count, j in enumerate(numbers)
    ]
    temp = []
    keyboard = []
    for num, btn in enumerate(x, start=1):
        temp.append(btn)
        if num % 3 == 0:
            keyboard.append(temp)
            temp = []
        if num == len(x):
            keyboard.append(temp)
    return keyboard
