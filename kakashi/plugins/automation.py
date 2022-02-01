import aiosqlite
from lightbulb.context import Context
from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.commands.prefix import (
    PrefixCommand,
    PrefixCommandGroup,
    PrefixSubCommand,
)
from lightbulb.commands.slash import SlashCommand, SlashCommandGroup, SlashSubCommand
from lightbulb.converters.special import EmojiConverter, TextableGuildChannelConverter
from lightbulb.checks import has_guild_permissions
from lightbulb.decorators import command, implements, add_checks, option, add_cooldown
from lightbulb.cooldowns import UserBucket
from hikari.channels import GuildTextChannel
from hikari.embeds import Embed
from hikari.events import StartedEvent
from hikari.permissions import Permissions
from kakashi.exts.hex import ColorHelper
from kakashi.exts.db_handler import MessageLogDatabase

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
async def automation_base(ctx: Context):
    await ctx.bot.help_command.send_help(ctx, ctx.command.plugin.name)


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
async def command(ctx: Context):
    """Set message log"""
    data = await MessageLogDatabase.get_data(ctx, ctx.bot)
    if not ctx.options.channel:
        if data:
            return await ctx.respond(
                embed=Embed(
                    description=f"Logged messages are being sent in <#{data}>",
                    color=ColorHelper.cyan,
                ),
                reply=True,
            )
        return await ctx.bot.help_command.send_help(ctx, ctx.command.name)
    if ctx.options.channel.id not in ctx.get_guild().get_channels():
        return await ctx.respond(
            embed=Embed(
                description=f"The channel must belong to the same server",
                color=ColorHelper.red,
            ),
            reply=True,
        )
    await MessageLogDatabase.insert_data(ctx, ctx.options.channel.id)
    await ctx.respond(
        embed=Embed(
            description=f"Set message log channel to {ctx.options.channel.mention}",
            color=ColorHelper.green,
        ),
        reply=True,
    )


def load(bot: BotApp):
    bot.add_plugin(automation)
