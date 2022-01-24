from hikari.emojis import Emoji, UnicodeEmoji, CustomEmoji
from lightbulb.commands.slash import SlashCommand
from lightbulb.plugins import Plugin
from lightbulb.decorators import implements, command, option, add_checks, add_cooldown
from lightbulb import checks
from lightbulb.commands.prefix import PrefixCommand
from lightbulb.context import Context
from lightbulb.app import BotApp
from lightbulb.cooldowns import UserBucket
from hikari.users import User
from hikari.guilds import Member, Role
from hikari.embeds import Embed
from hikari.permissions import Permissions
from kakashi.exts import ColorHelper, InfoEmbedHelper
from typing import Optional

# from hikari.interactions.base_interactions import InteractionMember

info_plugin = Plugin(
    name="Info",
    description="Module with various info commands about your server and users",
)


@info_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@option(name="user", description="Targetted User", required=False, type=Optional[User])
@command(
    name="avatar",
    description="View user's avatar ",
    aliases=["av", "pfp"],
    ephemeral=True,
)
@implements(PrefixCommand, SlashCommand)
async def av_cmd(ctx: Context):
    """Avatar command"""
    user = ctx.options.user or ctx.author
    await ctx.respond(
        embed=Embed(
            description=f"[Download]({user.avatar_url or user.default_avatar_url})",
            color=ColorHelper.blue,
        )
        .set_author(name=f"{user}'s AVATAR")
        .set_footer(
            text=f"Requested by : {ctx.author}",
            icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
        )
        .set_image(user.avatar_url or user.default_avatar_url)
    )


@info_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@option(
    name="member",
    description="Member to get information about",
    required=False,
    type=Member,
)
@command(
    name="userinfo",
    description="Get information about a mentioned member",
    aliases=["whois", "ui"],
)
@implements(PrefixCommand, SlashCommand)
async def whois_cmd(ctx: Context):
    """Info about mentioned user"""
    member = ctx.options.member or ctx.member
    await ctx.respond(
        embed=await InfoEmbedHelper.embed_for_member(ctx, member), reply=True
    )


@info_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@option(
    name="role", description="Role to get information about", required=True, type=Role
)
@command(
    name="roleinfo", description="Information about a mentioned role", aliases=["ri"]
)
@implements(PrefixCommand, SlashCommand)
async def roleinfo_cmd(ctx: Context):
    """Info about a role"""
    await ctx.respond(
        embed=await InfoEmbedHelper.embed_for_role(ctx, ctx.options.role), reply=True
    )


@info_plugin.command
@add_cooldown(10, 2, bucket=UserBucket)
@option(
    name="emoji",
    description="Emojo to get information about",
    type=Emoji,
    required=True,
)
@command(name="emoji", description="Infor about an Custom Emoji", aliases=["emojiinfo"])
@implements(PrefixCommand, SlashCommand)
async def emoji_info_cmd(ctx: Context):
    emoji: Emoji = ctx.options.emoji
    if isinstance(emoji, UnicodeEmoji):
        return await ctx.respond("This is a default discord Emoji", reply=True)
    emoji: CustomEmoji
    created_at = f'<t:{int(emoji.created_at.timestamp())}:R> ||{emoji.created_at.strftime("%#d %B %Y")}||'
    embed = Embed(
        color=ColorHelper.yellow,
        description=f"**Elasped name :** `{emoji.mention}`\n**Created :** {created_at}\n**Animated :** {emoji.is_animated}\n**ID :** {emoji.id} ",
    )
    embed.set_author(name=f"{emoji.name} Emoji", icon=emoji.url)
    embed.set_image(emoji.url)
    embed.set_footer(
        text=f"Requested by : {ctx.author}",
        icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
    )
    await ctx.respond(embed=embed, reply=True)


def load(bot: BotApp):
    bot.add_plugin(info_plugin)
