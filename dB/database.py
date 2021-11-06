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
    def __init__(self):
        super().__init__()

    # Sudo Things
    def add_sudo(self, chat_id: int, user_id: int):
        if user_id in self.get_sudos(chat_id):
            return
        cur.execute(f"INSERT INTO sudo_db VALUES ({chat_id}, {user_id})")
        conn.commit()

    def del_sudo(self, chat_id: int, user_id: int):
        cur.execute(f"DELETE FROM sudo_db WHERE user_id = {user_id} AND chat_id = {chat_id}")
        conn.commit()

    def get_sudos(self, chat_id: int):
        return [row[1] for row in cur.execute(f"SELECT * FROM sudo_db WHERE chat_id = {chat_id}")]

    def add_chat(self, owner_id: int = owners, chat_id: int = 0, lang: str = "en", video_quality: str = "medium"):
        already = self.get_chat(chat_id)
        already_chat_id = 0
        for ready in already:
            already_chat_id = ready["chat_id"]
        if not already_chat_id:
            cur.execute(f"INSERT INTO chat_db VALUES ({owner_id}, {chat_id}, '{lang}', '{video_quality.lower()}')")
            conn.commit()
            return True
        return True

    def get_chat(self, chat_id: int):
        results = cur.execute(f"SELECT * FROM chat_db WHERE chat_id = {chat_id}")
        final = []
        for result in results:
            res = result
            owner_id = res[0]
            chat_id = res[1]
            lang = res[2]
            video_quality = res[3]
            x = {
                "owner_id": owner_id,
                "chat_id": chat_id,
                "lang": lang,
                "video_quality": video_quality
            }
            final.append(x.copy())
        return final

    def del_chat(self, chat_id: int):
        cur.execute(f"DELETE FROM chat_db WHERE chat_id = {chat_id}")
        conn.commit()
        return True

    def set_chat_lang(self, chat_id: int, lang: str):
        cur.execute(f"""
                UPDATE chat_db
                SET lang = '{lang}'
                WHERE chat_id = {chat_id}
                """)
        conn.commit()
        return True

    def set_video_quality(self, chat_id: int, quality: str):
        cur.execute(f"""
                UPDATE chat_db
                SET video_quality = '{quality}'
                WHERE chat_id = {chat_id}
                """)
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
        return group, pm


db = Database()
