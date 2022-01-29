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
from kakashi.exts import ColorHelper
from aiohttp import ClientSession
from random import choice

fun_plugin = Plugin(name="Fun", description="Some fun commands")


async def fetch_meme():
    async with ClientSession() as session:
        res = await session.get(
            f"https://meme-api.herokuapp.com/gimme/{choice(['memes','dankmemes','me_irl','wholesomememes'])}"
        )
        data = await res.json()
        return data


@fun_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@command(name="meme", description="A random meme from reddit")
@implements(SlashCommand, PrefixCommand)
async def meme_cmd(ctx: Context):
    """Meme command"""
    nsfw = True
    while nsfw == True:
        """Avoiding Nsfw"""
        data = await fetch_meme()
        if not data["nsfw"]:
            nsfw = False

    embed = Embed(
        title=f"r/{data['subreddit']}",
        description=data["title"],
        color=ColorHelper.blue,
        url=f"https://reddit.com/r/{data['subreddit']}",
    ).set_author()
    embed.set_image(data["url"])
    embed.set_footer(
        text=f'👍 {data["ups"]} ups | Requested by {ctx.author}',
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )
    await ctx.respond(embed=embed, reply=True)


@fun_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@command(name="neko", description="A neko picture")
@implements(SlashCommand, PrefixCommand)
async def neko_cmd(ctx: Context):
    """Neko picture"""
    async with ClientSession() as session:
        res = await session.get("https://neko-love.xyz/api/v1/neko")
        data = await res.json()

    await ctx.respond(
        embed=(
            Embed(color=ColorHelper.pink)
            .set_image(data["url"])
            .set_author(
                name="Here's a neko for you!",
                icon=ctx.bot.get_me().avatar_url or ctx.bot.get_me().default_avatar_url,
            )
            .set_footer(
                text=f"Requested by {ctx.author}",
                icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
            )
        ),
        reply=True,
    )


def load(bot: BotApp):
    bot.add_plugin(fun_plugin)
