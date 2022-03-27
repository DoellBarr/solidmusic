from databases import Database


class Db:
    def __init__(self):
        self.db = Database("sqlite+aiosqlite:///native.db")

    async def connect(self):
        return await self.db.connect()

    async def disconnect(self):
        return await self.db.disconnect()

    async def init(self):
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_db
            (
                owner_id integer,
                chat_id integer,
                chat_lang text,
                media_quality text,
                admin_only boolean,
                del_cmd_mode boolean,
                player_mode boolean,
                duration_limit integer
            )
            """
        )
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS sudo_db
            (
                chat_id integer,
                user_id integer
            )
            """
        )


db = Db()
