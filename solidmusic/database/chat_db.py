from typing import List, Dict, Union
from .db import Db
from configs import config


class ChatDB(Db):
    async def add_chat(self, chat_id: int, lang: str = "en"):
        x = list(
            await self.db.fetch_all(
                query="select * from chat_db where chat_id = :chat_id",
                values={"chat_id": chat_id},
            )
        )
        if not x:
            await self.db.execute(
                "insert into chat_db values (:owner_id, :chat_id, :chat_lang, :media_quality, :admin_only, :del_cmd_mode, :player_mode, :duration_limit)",
                {
                    "owner_id": config.owner_id,
                    "chat_id": chat_id,
                    "chat_lang": lang,
                    "media_quality": "medium",
                    "admin_only": True,
                    "del_cmd_mode": True,
                    "player_mode": True,
                    "duration_limit": 0,
                },
            )
            return "chat_success_added"
        return "chat_already_added"

    @staticmethod
    def _get(chat: List) -> Dict[str, str]:
        (
            owner_id,
            chat_id,
            chat_lang,
            media_quality,
            admin_only,
            del_cmd_mode,
            player_mode,
            duration_limit,
        ) = chat
        return {
            "owner_id": owner_id,
            "chat_id": chat_id,
            "chat_lang": chat_lang,
            "media_quality": media_quality,
            "admin_only": bool(admin_only),
            "del_cmd_mode": bool(del_cmd_mode),
            "player_mode": bool(player_mode),
            "duration_limit": False if duration_limit == 0 else duration_limit,
        }

    async def get_chat(self, chat_id: int) -> Union[Dict, Dict[str, str]]:
        fetch = await self.db.fetch_one(
            "select * from chat_db where chat_id = :chat_id", {"chat_id": chat_id}
        )
        result = list(fetch) if fetch else {}
        return self._get(result) if result else {}

    async def check_chat(self, chat_id: int):
        chat = await self.get_chat(chat_id)
        if not chat:
            await self.add_chat(chat_id)
            return await self.get_chat(chat_id)
        return chat

    async def del_chat(self, chat_id: int):
        x = await self.db.fetch_one(
            "select * from chat_db where chat_id = :chat_id", {"chat_id": chat_id}
        )
        if not x:
            return "chat_already_deleted"
        await self.db.execute(
            "delete from chat_db where chat_id = :chat_id", {"chat_id": chat_id}
        )
        return "chat_success_deleted"

    async def set_lang(self, chat_id: int, lang: str):
        chat = await self.check_chat(chat_id)
        if chat["chat_lang"] == lang:
            return "lang_already_used"
        await self.db.execute(
            "update chat_db set chat_lang = :chat_lang where chat_id = :chat_id",
            {"chat_lang": lang, "chat_id": chat_id},
        )
        return "lang_changed"

    async def set_quality(self, chat_id: int, quality: str):
        chat = await self.check_chat(chat_id)
        if chat["media_quality"] == quality:
            return "quality_already_used"
        await self.db.execute(
            "update chat_db set media_quality = :media_quality where chat_id = :chat_id",
            {"media_quality": quality, "chat_id": chat_id},
        )
        return "quality_changed"

    async def set_admin_mode(self, chat_id: int, only_admin: bool):
        chat = await self.check_chat(chat_id)
        if chat["admin_only"] and chat["admin_only"] == only_admin:
            return "only_admin_already_set"
        if not chat["admin_only"] and chat["admin_only"] == only_admin:
            return "all_member_already_set"
        await self.db.execute(
            "update chat_db set admin_only = :admin_only where chat_id = :chat_id",
            {"admin_only": only_admin, "chat_id": chat_id},
        )
        return "only_admin_changed" if only_admin else "all_member_changed"

    async def set_del_cmd_mode(self, chat_id: int, del_cmd_mode: bool):
        chat = await self.check_chat(chat_id)
        if chat["del_cmd_mode"] == del_cmd_mode:
            return "del_cmd_mode_already_set"
        await self.db.execute(
            "update chat_db set del_cmd_mode = :del_cmd_mode where chat_id = :chat_id",
            {"del_cmd_mode": del_cmd_mode, "chat_id": chat_id},
        )
        return "del_cmd_changed"

    async def set_player_mode(self, chat_id: int, player_mode: bool):
        chat = await self.check_chat(chat_id)
        if chat["player_mode"] == player_mode:
            return "player_mode_already_set"
        await self.db.execute(
            "update chat_db set player_mode = :player_mode where chat_id = :chat_id",
            {"player_mode": player_mode, "chat_id": chat_id},
        )
        return "player_mode_changed"

    async def set_duration_limit(self, chat_id: int, duration_limit: int):
        chat = await self.check_chat(chat_id)
        if int(chat["duration_limit"]) == duration_limit:
            return "duration_limit_already_set"
        await self.db.execute(
            "update chat_db set duration_limit = :duration_limit where chat_id = :chat_id",
            {"duration_limit": duration_limit, "chat_id": chat_id},
        )
        return "duration_limit_changed"

    async def set_gcast(self, chat_id: int, gcast_type: str):
        chat = await self.get_chat(chat_id)
        if gcast_type == chat.get("gcast_type"):
            return "gcast_already_set"
        await self.db.execute(
            "update chat_db set gcast_type = :gcast_type where chat_id = :chat_id",
            {"gcast_type": gcast_type, "chat_id": chat_id},
        )
        return "gcast_changed"


chat_db = ChatDB()
