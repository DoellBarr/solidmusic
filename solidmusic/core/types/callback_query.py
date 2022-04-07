from typing import Match
import pyrogram
from pyrogram import types
from pyrogram.types import CallbackQuery as RawCallbackQuery
from solidmusic.core.types.message import Message

from solidmusic.database.lang_utils import gm


class CallbackQuery(RawCallbackQuery):
    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        id: str,
        from_user: types.User,
        chat_instance: str,
        message: Message = None,
        inline_message_id: str = None,
        data: str | bytes = None,
        game_short_name: str = None,
        matches: list[Match] = None
    ):
        super().__init__(
            client=client,
            id=id,
            from_user=from_user,
            chat_instance=chat_instance,
            message=message,
            inline_message_id=inline_message_id,
            data=data,
            game_short_name=game_short_name,
            matches=matches
        )

    async def edit_msg(
        self,
        key: str,
        format_key: list[str] = None,
        parse_mode: None | str = object,
        disable_web_page_preview: bool = True,
        reply_markup: types.InlineKeyboardMarkup = None
    ) -> Message | bool:
        """Edit the text of messages attached to callback queries.

                Bound method *edit_message_text* of :obj:`~pyrogram.types.CallbackQuery`.

                Parameters:
                    key (``str``):
                        The key from a language in yaml file

                    format_key (``list[str]``):
                        Format key for the {} in the language string

                    parse_mode (``str``, *optional*):
                        By default, texts are parsed using both Markdown and HTML styles.
                        You can combine both syntaxes together.
                        Pass "markdown" or "md" to enable Markdown-style parsing only.
                        Pass "html" to enable HTML-style parsing only.
                        Pass None to completely disable style parsing.

                    disable_web_page_preview (``bool``, *optional*):
                        Disables link previews for links in this message.

                    reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                        An InlineKeyboardMarkup object.

                Returns:
                    :obj:`~pyrogram.types.Message` | ``bool``: On success, if the edited message was sent by the bot, the edited
                    message is returned, otherwise True is returned (message sent via the bot, as inline query result).

                Raises:
                    RPCError: In case of a Telegram RPC error.
                """
        chat_id = self.message.chat.id
        text = await gm(chat_id, key, format_key)
        if self.inline_message_id is None:
            return await self._client.edit_message_text(
                chat_id=chat_id,
                message_id=self.message.message_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )
        return await self._client.edit_inline_text(
            inline_message_id=self.inline_message_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )

    edit = edit_msg

    async def answer_msg(
        self,
        key: str = None,
        format_key: list[str] = None,
        show_alert: bool = None,
        url: str = None,
        cache_time: int = 0
    ):
        text = await gm(self.message.chat.id, key, format_key)
        return await self._client.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )

    answer = answer_msg
