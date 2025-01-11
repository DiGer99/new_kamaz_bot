from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class IdsAdimn:
    ids: list


@dataclass
class Config:
    tg_bot: TgBot
    admins: IdsAdimn


def load_config(path: str | None = None):
    env = Env()
    env.read_env()
    return Config(
        tg_bot=TgBot(env("BOT_TOKEN")),
        admins=IdsAdimn(env("ADMINS"))
        )