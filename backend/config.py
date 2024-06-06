from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret: str = "effd59a38c8593085c62f9c6d6e87fcbe9633e85ef16c52f"
    database_uri: str = "sqlite:///app.db"
    token_url: str = "/auth/token"


DEFAULT_SETTINGS = Settings()
