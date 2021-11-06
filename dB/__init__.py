import sqlite3

conn = sqlite3.connect("solid.db")
cur = conn.cursor()


cur.execute(
    """
    CREATE TABLE IF NOT EXISTS chat_db
    (owner_id integer, chat_id integer, lang text, video_quality text);
    """
)
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sudo_db 
    (chat_id integer, user_id integer);
    """
)
