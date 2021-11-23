from . import conn, cur
from .sudo_db import SudoDB
from .chat_db import ChatDB
from configs import config

owners = config.OWNER_ID


class Methods(
    ChatDB,
    SudoDB,
):
    pass


class Database(Methods):
    # Sudo Things
    def add_sudo(self, chat_id: int, user_id: int):
        if user_id in self.get_sudos(chat_id):
            return "already_become_sudo"
        cur.execute(
            "INSERT INTO sudo_db VALUES (?, ?)",
            (chat_id, user_id)
        )
        conn.commit()
        return "added_sudo"

    def del_sudo(self, chat_id: int, user_id: int):
        if user_id not in self.get_sudos(chat_id):
            return "already_deleted_sudo"
        cur.execute(
            "DELETE FROM sudo_db WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        conn.commit()
        return "deleted_sudo"

    def get_sudos(self, chat_id: int):
        return [
            row[1]
            for row in cur.execute(
                "SELECT * FROM sudo_db WHERE chat_id = ?",
                (chat_id,)
            )
        ]

    def add_chat(
        self,
        chat_id: int = 0,
        lang: str = "en",
        owner_id: int = owners,
        video_quality: str = "medium",
        only_admin: bool = False,
    ):
        already = self.get_chat(chat_id)
        already_chat_id = 0
        for ready in already:
            already_chat_id = ready["chat_id"]
        if not already_chat_id:
            cur.execute(
                "INSERT INTO chat_db VALUES (?, ?, ?, ?, ?)",
                (owner_id, chat_id, f"{lang}", f"{video_quality.lower()}", only_admin)
            )
            conn.commit()
            return True
        return False

    def get_chat(self, chat_id: int):
        results = cur.execute("SELECT * FROM chat_db WHERE chat_id = ?", (chat_id,))
        final = []
        for result in results:
            res = result
            owner_id = res[0]
            chat_id = res[1]
            lang = res[2]
            video_quality = res[3]
            only_admin: bool = res[4]
            admin = bool(only_admin)
            x = {
                "owner_id": owner_id,
                "chat_id": chat_id,
                "lang": lang,
                "video_quality": video_quality,
                "only_admin": admin,
            }
            final.append(x.copy())
        return final

    def del_chat(self, chat_id: int):
        try:
            self.get_chat(chat_id)
            cur.execute("DELETE FROM chat_db WHERE chat_id = ? ", (chat_id,))
            conn.commit()
            return True
        except KeyError:
            return False

    def set_chat_lang(self, chat_id: int, lang: str):
        cur.execute(
            """
                UPDATE chat_db
                SET lang = ?
                WHERE chat_id = ?
            """,
            (f"{lang}", chat_id,)
        )
        conn.commit()
        return True

    def set_video_quality(self, chat_id: int, quality: str):
        cur.execute(
            """
            UPDATE chat_db
            SET video_quality = ?
            WHERE chat_id = ?
            """,
            (f"{quality}", chat_id,)
        )
        conn.commit()
        return True

    def get_stats(self):
        chats = cur.execute("SELECT * FROM chat_db")
        group = pm = 0
        for chat in chats:
            chat_id = str(chat[0])
            if chat_id.startswith("-"):
                group += 1
            else:
                pm += 1
        return {"groups": group, "pm": pm}

    def set_only_admin_stream(self, chat_id: int, only_admin: bool):
        cur.execute(
            """
            UPDATE chat_db
            SET stream_only_admin = ?
            WHERE chat_id = ?
            """,
            (only_admin, chat_id,)
        )
        conn.commit()
        return True


db = Database()
