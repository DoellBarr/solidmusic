from .db import Db


class SudoDB(Db):
    async def get_sudos(self, chat_id: int):
        return [
            row[1]
            for row in await self.db.fetch_all(
                "select * from sudo_db where chat_id = :chat_id", {"chat_id": chat_id}
            )
        ]

    async def add_sudo(self, chat_id: int, user_id: int):
        if user_id in await self.get_sudos(chat_id):
            return "already_become_sudo"
        await self.db.execute(
            "insert into sudo_db values (:chat_id, :user_id)",
            {"chat_id": chat_id, "user_id": user_id},
        )
        return "added_sudo"

    async def del_sudo(self, chat_id: int, user_id: int):
        if user_id not in await self.get_sudos(chat_id):
            return "already_deleted_sudo"
        await self.db.execute(
            "delete from sudo_db where chat_id = :chat_id and user_id = :user_id",
            {"chat_id": chat_id, "user_id": user_id},
        )
        return "deleted_sudo"


sudo_db = SudoDB()
