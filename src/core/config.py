from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_uri: str = "sqlite+aiosqlite:///./db.sqlite3"
