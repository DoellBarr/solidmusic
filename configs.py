import heroku3
from dotenv import load_dotenv
from os import path, getenv


if path.exists("local.env"):
    load_dotenv("local.env")
else:
    load_dotenv()


def get_heroku_git_url(api_key: str, app_name: str):
    if not api_key or app_name:
        return None
    heroku = heroku3.from_key(api_key)
    heroku_apps = heroku.apps()
    app = None
    for heroku_app in heroku_apps:
        if heroku_app.name == app_name:
            app = heroku_app
            break
    if not app:
        return None
    return app.git_url.replace("https://", f"https://api:{api_key}@")


class Config:
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH", "abc123")
    BOT_TOKEN = getenv("BOT_TOKEN", "1234:abcd")
    SESSION = getenv("SESSION", "session")
    OWNER_ID = int(getenv("OWNER_ID", "1952053555"))
    SUPPORT = getenv("SUPPORT", "https://t.me/solidprojects_chat")
    CHANNEL = getenv("CHANNEL", "https://t.me/solidprojects")
    HEROKU_APP = getenv("HEROKU_APP", None)
    HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)
    HEROKU_GIT_URL = get_heroku_git_url(HEROKU_API_KEY, HEROKU_APP)


config = Config()
