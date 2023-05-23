from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_password: str | None = None
    db_user: str = "jsong"
    db_name: str = "tweeter"

    api_host = "localhost"
    api_port = 5005

    redis_host = "localhost"
    redis_port = 6379

    def get_api_url(self):
        return f"http://{self.api_host}:{self.api_port}"

    def get_postgres_uri(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_redis_uri(self):
        return {
            "host": self.redis_host,
            "port": self.redis_port,
        }


def get_settings():
    return Settings()
