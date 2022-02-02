from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.context import Context
from lightbulb.commands import PrefixCommand
from lightbulb.decorators import command, implements, option

from kakashi.helpers import MyHelp

help_plugin = Plugin(name="Help Plugin", description="Help Command Plugin")
# help_plugin.bot.help_command = MyHelp()


@help_plugin.command
@option(name="obj", description="object to send help of", required=False)
@command(name="h", description="aliases help")
@implements(PrefixCommand)
async def help_alias(context: Context) -> None:
    await context.bot.help_command.send_help(context, context.options.obj)


def load(bot: BotApp):
    bot.add_plugin(help_plugin)


def unload(bot: BotApp):
    bot.remove_plugin(help_plugin)
