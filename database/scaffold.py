import sqlite3


class Scaffold:
    def __init__(self):
        self.conn = sqlite3.connect("solid.db")
        self.cur = self.conn.cursor()

    def init(self):
        cur = self.cur
        try:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_db
                (
                owner_id integer, 
                chat_id integer, 
                lang text, 
                quality text, 
                admin_only boolean, 
                gcast_type text,
                del_cmd_mode boolean,
                player_mode boolean,
                duration integer
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sudo_db
                (chat_id integer, user_id integer);
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD duration integer
                DEFAULT 0
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD player_mode boolean
                DEFAULT 1
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD del_cmd_mode boolean
                DEFAULT 1
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD gcast_type text
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD admin_only boolean
                """
            )
            cur.execute(
                """
                ALTER TABLE chat_db
                ADD quality text
                """
            )
        except sqlite3.OperationalError:
            pass

    def close(self):
        return self.cur.close()
