from .scaffold import Scaffold


class SudoDB(Scaffold):
    def get_sudos(self, chat_id: int):
        return [
            row[1]
            for row in self.cur.execute(
                "SELECT * FROM sudo_db WHERE chat_id = ?", (chat_id,)
            )
        ]

    def add_sudo(self, chat_id: int, user_id: int):
        if user_id in self.get_sudos(chat_id):
            return "already_become_sudo"
        self.cur.execute(
            "INSERT INTO sudo_db VALUES (?, ?)",
            (
                chat_id,
                user_id,
            ),
        )
        self.conn.commit()
        return "added_sudo"

    def del_sudo(self, chat_id: int, user_id: int):
        if user_id not in self.get_sudos(chat_id):
            return "already_deleted_sudo"
        self.cur.execute(
            "DELETE FROM sudo_db WHERE chat_id = ? AND user_id = ?",
            (
                chat_id,
                user_id,
            ),
        )
        self.conn.commit()
        return "deleted_sudo"


sudo_db = SudoDB()
