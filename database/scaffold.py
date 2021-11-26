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
                gcast_type text
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
