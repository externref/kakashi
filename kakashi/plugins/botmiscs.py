import aiosqlite
from typing import Optional
from datetime import datetime
from platform import python_version

from lightbulb import checks
from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.context import Context
from lightbulb.cooldowns import UserBucket
from lightbulb.commands.slash import SlashCommand
from lightbulb.commands.base import OptionModifier
from lightbulb.commands.prefix import PrefixCommand
from lightbulb.decorators import implements, command, option, add_checks, add_cooldown

from hikari.embeds import Embed
from hikari.messages import Message
from hikari.events import StartedEvent
from hikari.permissions import Permissions

from kakashi.helpers import PrefixHandler, ColorHelper


botmisc = Plugin(
    name="Bot Related", description="Commands related to Bot setup and data"
)


@botmisc.listener(StartedEvent)
async def connect_to_prefix(event: StartedEvent) -> None:
    botmisc.bot.prefix_database = await aiosqlite.connect("database/guilds.db")
    print("Connected to Prefix database !")


@botmisc.command
@add_cooldown(10, 2, bucket=UserBucket)
@command(name="ping", description="Sends bot's latency", aliases=["latency"])
@implements(PrefixCommand, SlashCommand)
async def ping(context: Context) -> None:
    """Bot's Latency"""
    await context.respond(
        f"🏓 Pong `{round(context.bot.heartbeat_latency *1000 , 2)}` ms !"
    )


@botmisc.command
@add_cooldown(10, 2, bucket=UserBucket)
@add_checks(checks.has_guild_permissions(Permissions.MANAGE_GUILD))
@option(
    name="new_prefix",
    description="The new prefix for server",
    required=True,
    modifier=OptionModifier.CONSUME_REST,
)
@command(name="prefix", description="Change prefix for the server")
@implements(PrefixCommand, SlashCommand)
async def change_prefix(context: Context) -> Optional[Message]:
    """Change prefix for your server"""
    prefix = context.options.new_prefix

    prefix: str
    if any([char for char in prefix if char in ["#", "@", "`", ":", "/"]]):
        return await context.respond(
            embed=Embed(
                description=f"Prefixes Cannot have the following contents : `#` , `@` , `:` , `/` , `",
                color=ColorHelper.red,
            ),
            reply=True,
        )
    await PrefixHandler.prefix_setter(context, prefix)
    await context.respond(
        embed=Embed(
            description=f"Changed Server Prefix to {prefix}",
            color=ColorHelper.green,
        ),
        reply=True,
    )


@botmisc.command
@add_cooldown(10, 2, bucket=UserBucket)
@command(name="botinfo", description="Stats and info about bot", ephemeral=True)
@implements(PrefixCommand, SlashCommand)
async def botstats_command(context: Context) -> None:
    """Some stats and info about bot"""
    embed = (
        Embed(color=ColorHelper.cyan)
        .set_author(
            name=f"{context.bot.get_me().username.upper()} BOT",
            icon=context.bot.get_me().avatar_url
            or context.bot.get_me().default_avatar_url,
        )
        .set_thumbnail(
            context.bot.get_me().avatar_url or context.bot.get_me().default_avatar_url
        )
        .add_field(
            name="Made with",
            value=f"⤷{context.bot.cache.get_emoji(840976596475445297)} [`python {python_version()}`](https://www.python.org/)\n⤷{context.bot.cache.get_emoji(929936527285432330)} [`hikari {context.bot.hikari_version}`](https://www.hikari-py.dev/)\n⤷[💡 `hikari-lightbulb {context.bot.lightbulb_version}`](https://hikari-lightbulb.readthedocs.io/en/latest/)",
        )
        .add_field(
            name=f"{context.bot.cache.get_emoji(929939525428445265)} Source Info",
            value=f"⤷Bot Source : [sarthak-py/Winky](https://github.com/sarthak-py/Winky)\n⤷Code Style : black",
        )
    )
    embed.description = f"```yaml\nUptime : {(datetime.now()-context.bot.boot_datetime)}\nServers : {len(context.bot.cache.get_guilds_view())}\nCached Users : {len(context.bot.cache.get_users_view())}\n\n```"
    await context.respond(embed=embed, reply=True)


def load(bot: BotApp) -> None:
    bot.add_plugin(botmisc)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(botmisc)
