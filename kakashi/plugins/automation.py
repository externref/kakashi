import aiosqlite
from typing import Optional

from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.context import Context
from lightbulb.commands.prefix import (
    PrefixCommand,
    PrefixCommandGroup,
    PrefixSubCommand,
)
from lightbulb.cooldowns import UserBucket
from lightbulb.checks import has_guild_permissions
from lightbulb.commands.slash import SlashCommand, SlashCommandGroup, SlashSubCommand
from lightbulb.converters.special import EmojiConverter, TextableGuildChannelConverter
from lightbulb.decorators import command, implements, add_checks, option, add_cooldown

from hikari.embeds import Embed
from hikari.messages import Message
from hikari.events import StartedEvent
from hikari.permissions import Permissions
from hikari.channels import GuildTextChannel

from kakashi.helpers.hex import ColorHelper
from kakashi.helpers.db_handler import MessageLogDatabase

automation = Plugin(
    name="Automation", description="All automations you need for your server"
)


@automation.listener(StartedEvent)
async def connect_to_prefix(event: StartedEvent):
    automation.bot.automation_database = await aiosqlite.connect(
        "database/automations.db"
    )
    print("Connected to Automation database !")


@automation.command
@command(
    name="automation", description="Automation Commands for your server", hidden=True
)
@implements(PrefixCommand)
async def automation_base(context: Context):
    await context.bot.help_command.send_help(context, context.command.plugin.name)


@automation.command
@add_cooldown(10, 2, bucket=UserBucket)
@add_checks(has_guild_permissions(Permissions.MANAGE_GUILD))
@option(
    name="channel",
    description="Channel to send deleted messages in",
    type=TextableGuildChannelConverter,
    required=False,
)
@command(
    name="messagelogs",
    aliases=["msglogs"],
    description="Setup Logging Deleted messages in a channel",
)
@implements(PrefixCommand, SlashCommand)
async def msg_logs_command(context: Context) -> Optional[Message]:
    """Set message log"""
    data = await MessageLogDatabase.get_data(context, context.bot)
    if not context.options.channel:
        if data:
            return await context.respond(
                embed=Embed(
                    description=f"Logged messages are being sent in <#{data}>",
                    color=ColorHelper.cyan,
                ),
                reply=True,
            )
        return await context.bot.help_command.send_help(context, context.command.name)
    if context.options.channel.id not in context.get_guild().get_channels():
        return await context.respond(
            embed=Embed(
                description=f"The channel must belong to the same server",
                color=ColorHelper.red,
            ),
            reply=True,
        )
    await MessageLogDatabase.insert_data(context, context.options.channel.id)
    await context.respond(
        embed=Embed(
            description=f"Set message log channel to {context.options.channel.mention}",
            color=ColorHelper.green,
        ),
        reply=True,
    )


def load(bot: BotApp) -> None:
    bot.add_plugin(automation)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(automation)
