import asyncio

from pyrogram import types, raw
from pyrogram.types import Message as RawMessage

from solidmusic.database.lang_utils import gm


class Message(RawMessage):
    def __init__(self, *, message_id: int):
        super().__init__(message_id=message_id)

    async def reply_msg(
        self,
        key: str,
        format_key: list[str] = None,
        delete_time: int = 0,
        quote: bool = None,
        parse_mode: str | object = object,
        entities: list[types.MessageEntity] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        protect_content: bool = None,
        reply_markup=None,
    ) -> "Message":
        text = await gm(self.chat.id, key, format_key)
        if quote is None:
            quote = self.chat.type != "private"
        if reply_to_message_id is None and quote:
            reply_to_message_id = self.message_id
        msg = await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup,
        )
        if delete_time:
            await asyncio.sleep(delete_time)
            return await msg.delete()
        return msg

    reply = reply_msg

    async def view_msg(self, chat_id: int | str):
        peer = await self._client.resolve_peer(chat_id)
        return await self._client.send(
            raw.functions.messages.GetMessagesViews(
                peer=peer,
                id=[self.message_id],
                increment=True
            )
        )