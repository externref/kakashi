import aiosqlite
from lightbulb.commands.slash import SlashCommand
from lightbulb.plugins import Plugin
from lightbulb.decorators import implements, command, option, add_checks, add_cooldown
from lightbulb.cooldowns import UserBucket
from lightbulb import checks
from lightbulb.commands.prefix import PrefixCommand
from lightbulb.context import Context
from lightbulb.app import BotApp
from lightbulb.commands.base import OptionModifier
from hikari.embeds import Embed
from hikari.events import StartedEvent
from hikari.permissions import Permissions
from kakashi.exts import PrefixHandler, ColorHelper
from datetime import datetime
from platform import python_version


botmisc = Plugin(
    name="Bot Related", description="Commands related to Bot setup and data"
)


@botmisc.listener(StartedEvent)
async def connect_to_prefix(event: StartedEvent):
    botmisc.bot.prefix_database = await aiosqlite.connect("database/guilds.db")
    print("Connected to database !")


@botmisc.command
@add_cooldown(10, 2, bucket=UserBucket)
@command(name="ping", description="Sends bot's latency", aliases=["latency"])
@implements(PrefixCommand, SlashCommand)
async def ping(ctx: Context):
    """Bot's Latency"""
    await ctx.respond(f"🏓 Pong `{round(ctx.bot.heartbeat_latency *1000 , 2)}` ms !")


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
async def change_prefix(ctx: Context):
    """Change prefix for your server"""
    prefix = ctx.options.new_prefix

    prefix: str
    if any([char for char in prefix if char in ["#", "@", "`", ":", "/"]]):
        return await ctx.respond(
            embed=Embed(
                description=f"Prefixes Cannot have the following contents : `#` , `@` , `:` , `/` , `",
                color=ColorHelper.red,
            ),
            reply=True,
        )
    await PrefixHandler.prefix_setter(ctx, prefix)
    await ctx.respond(
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
async def botstats_command(ctx: Context):
    """Some stats and info about bot"""
    embed = (
        Embed(color=ColorHelper.cyan)
        .set_author(
            name=f"{ctx.bot.get_me().username.upper()} BOT",
            icon=ctx.bot.get_me().avatar_url or ctx.bot.get_me().default_avatar_url,
        )
        .set_thumbnail(
            ctx.bot.get_me().avatar_url or ctx.bot.get_me().default_avatar_url
        )
        .add_field(
            name="Made with",
            value=f"⤷{ctx.bot.cache.get_emoji(840976596475445297)} [`python {python_version()}`](https://www.python.org/)\n⤷{ctx.bot.cache.get_emoji(929936527285432330)} [`hikari {ctx.bot.hikari_version}`](https://www.hikari-py.dev/)\n⤷[💡 `hikari-lightbulb {ctx.bot.lightbulb_version}`](https://hikari-lightbulb.readthedocs.io/en/latest/)",
        )
        .add_field(
            name=f"{ctx.bot.cache.get_emoji(929939525428445265)} Source Info",
            value=f"⤷Bot Source : [sarthak-py/Winky](https://github.com/sarthak-py/Winky)\n⤷Code Style : black",
        )
    )
    embed.description = f"```yaml\nUptime : {(datetime.now()-ctx.bot.boot_datetime)}\nServers : {len(ctx.bot.cache.get_guilds_view())}\nCached Users : {len(ctx.bot.cache.get_users_view())}\n\n```"
    await ctx.respond(embed=embed, reply=True)


def load(bot: BotApp):
    bot.add_plugin(botmisc)
