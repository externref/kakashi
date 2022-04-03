from lightbulb.plugins import Plugin
from lightbulb.context.base import Context
from lightbulb.commands.slash import SlashCommand
from lightbulb.commands.prefix import PrefixCommand
from lightbulb.decorators import command, option, implements

from hikari.embeds import Embed

from ..core.bot import Kakashi


class General(Plugin):
    def __init__(self):
        self.bot: Kakashi
        super().__init__(name="General Commands", description="General bot commands.")


general = General()


@general.command
@command(name="ping", description="Bot's latency in ms.")
@implements(PrefixCommand, SlashCommand)
async def _ping(context: Context) -> None:
    embed = Embed(color=general.bot.color, description="Getting Bot Ping.")
    await context.respond(embed=embed)


# await context.edit_last_response()


def load(bot: Kakashi):
    bot.add_plugin(general)
