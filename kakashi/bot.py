from datetime import datetime

from lightbulb.app import BotApp, when_mentioned_or
from lightbulb.checks import bot_has_guild_permissions

from hikari.intents import Intents
from hikari.permissions import Permissions

from .helpers import initialise_databases, PrefixHandler


class Kakashi(BotApp):
    def __init__(self, token):
        super().__init__(
            token=token,
            intents=Intents.ALL,
            prefix=when_mentioned_or(PrefixHandler.prefix_getter),
            help_slash_command=True,
        )
        initialise_databases()
        self.boot_datetime = datetime.now()
        self.load_extensions("lightbulb.ext.filament.exts.superuser")
        self.load_extensions_from("kakashi/plugins")
        self.check(
            bot_has_guild_permissions(
                Permissions.EMBED_LINKS,
                Permissions.SEND_MESSAGES,
                Permissions.ATTACH_FILES,
                Permissions.READ_MESSAGE_HISTORY,
            )
        )


if __name__ == "__main__":
    Kakashi = Kakashi()
