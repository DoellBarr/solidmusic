from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from solidmusic.core.client import Client, bot
from solidmusic.core.types import Message
from solidmusic.database.lang_utils import gm
from solidmusic.functions.markup_button import start_markup
from solidmusic.functions.yt_utils import download_yt_thumbnails, get_yt_details


@Client.on_message(filters.command("start"))
async def pm_start(_, message: Message):
    me = await bot.get_me()
    bot_username = me.username
    bot_name = me.first_name
    chat_id = message.chat.id
    mention = message.from_user.mention
    user_id = message.from_user.id
    if message.chat.type == "private":
        if len(message.command) == 1:
            return await bot.send_message(
                chat_id,
                "pm_greet",
                format_key=str(mention),
                markup=start_markup(chat_id, bot_username),
                delete=0
            )
        if len(message.command) >= 2:
            query = message.command[1]
            if query.startswith("ytinfo_"):
                link = query.split("ytinfo_")[1]
                details = await get_yt_details(link)
                thumb_url = details["thumbnail"]
                thumb_file = await download_yt_thumbnails(thumb_url, user_id)
                result_text = f"""
{await gm(chat_id, 'track_info')}
📌 **{await gm(chat_id, 'yt_title')}**: {details['title']}
🕰 **{await gm(chat_id, 'duration')}**: {details['duration']}
👍 **{await gm(chat_id, 'yt_likes')}**: {details['likes']}
⭐ **{await gm(chat_id, 'yt_rating')}**: {details['rating']}
"""
                return await message.reply_photo(
                    thumb_file,
                    caption=result_text,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"🎥 {await gm(chat_id, 'watch_on_yt')}",
                                    url=f"https://www.youtube.com/watch?v={details['link']}",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    f"🗑 {await gm(chat_id, 'close_btn_name')}",
                                    callback_data="close",
                                )
                            ],
                        ]
                    ),
                )
            if query.startswith("help"):
                return await message.reply(
                    await gm(chat_id, "helpmusic"),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"{await gm(chat_id, 'commands')}",
                                    url="https://telegra.ph/The-Bot-Command-11-14",
                                )
                            ]
                        ]
                    ),
                    disable_web_page_preview=True,
                )
    if message.chat.type in ["group", "supergroup"]:
        await message.reply(
            "chat_greet", [mention, bot_name],
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            await gm(message.chat.id, "group_buttn"),
                            url=f"https://t.me/{bot_username}?start=help",
                        )
                    ]
                ],
            ),
            disable_web_page_preview=True,
        )


__cmds__ = ["start"]
__help__ = {
    "start": "help_start"
}
