import os
from datetime import datetime, timedelta

from lightbulb.app import BotApp, when_mentioned_or

from ..database.prefix import PrefixHandler


def get_token():
    import dotenv

    dotenv.load_dotenv()
    return os.getenv("TOKEN")


class Kakashi(BotApp):
    def __init__(self):
        self.prefix_handler = PrefixHandler("k!")
        super().__init__(
            token=get_token(),
            prefix=when_mentioned_or(self.prefix_handler.get_prefix),
            help_slash_command=True,
        )
        self._boot_time = datetime.now()
        self.load_extensions_from("src/extensions")

    @property
    def uptime(self) -> timedelta:
        return datetime.now() - self._boot_time
