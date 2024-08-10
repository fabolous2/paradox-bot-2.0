import toml
from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas import AdminConfig, WebConfig


class TomlConfig(BaseModel):
    admin: AdminConfig
    web: WebConfig


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    CONFIG_PATH: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


def load_toml_config() -> TomlConfig:
    with open(settings.CONFIG_PATH) as fd:
        cfg = TomlConfig.model_validate(toml.load(fd))
        return cfg


dev_config = load_toml_config()
