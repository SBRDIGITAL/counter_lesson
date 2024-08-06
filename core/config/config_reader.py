from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class BotSettings(BaseSettings):
    BOT_TOKEN: SecretStr


    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='UTF-8')


config = BotSettings()