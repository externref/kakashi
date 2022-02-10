from typing import Optional

from lightbulb import checks
from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.context import Context
from lightbulb.cooldowns import UserBucket
from lightbulb.commands.slash import SlashCommand
from lightbulb.commands.prefix import PrefixCommand
from lightbulb.decorators import implements, command, option, add_checks, add_cooldown

from hikari.users import User
from hikari.embeds import Embed
from hikari.messages import Message
from hikari.guilds import Member, Role
from hikari.permissions import Permissions
from hikari.emojis import Emoji, UnicodeEmoji, CustomEmoji

from kakashi.helpers import ColorHelper, InfoEmbedHelper


# from hikari.interactions.base_interactions import InteractionMember

info_plugin = Plugin(
    name="info",
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
async def av_cmd(context: Context) -> None:
    """Avatar command"""
    user = context.options.user or context.author
    await context.respond(
        embed=Embed(
            description=f"[Download]({user.avatar_url or user.default_avatar_url})",
            color=await ColorHelper.color_for_current(context, context.bot),
        )
        .set_author(name=f"{user}'s AVATAR")
        .set_footer(
            text=f"Requested by : {context.author}",
            icon=context.author.avatar_url or context.author.default_avatar_url,
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
async def whois_cmd(context: Context) -> None:
    """Info about mentioned user"""
    member = context.options.member or context.member
    await context.respond(
        embed=await InfoEmbedHelper.embed_for_member(context, member), reply=True
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
async def roleinfo_cmd(context: Context) -> None:
    """Info about a role"""
    await context.respond(
        embed=await InfoEmbedHelper.embed_for_role(context, context.options.role),
        reply=True,
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
async def emoji_info_cmd(context: Context) -> Optional[Message]:
    """Information about an emoji"""
    emoji: Emoji = context.options.emoji
    if isinstance(emoji, UnicodeEmoji):
        return await context.respond("This is a default discord Emoji", reply=True)
    emoji: CustomEmoji
    created_at = f'<t:{int(emoji.created_at.timestamp())}:R> ||{emoji.created_at.strftime("%#d %B %Y")}||'
    embed = Embed(
        color=await ColorHelper.color_for_current(context, context.bot),
        description=f"**Elasped name :** `{emoji.mention}`\n**Created :** {created_at}\n**Animated :** {emoji.is_animated}\n**ID :** {emoji.id} ",
    )
    embed.set_author(name=f"{emoji.name} Emoji", icon=emoji.url)
    embed.set_image(emoji.url)
    embed.set_footer(
        text=f"Requested by : {context.author}",
        icon=context.author.avatar_url or context.author.default_avatar_url,
    )
    await context.respond(embed=embed, reply=True)


def load(bot: BotApp):
    bot.add_plugin(info_plugin)


def unload(bot: BotApp):
    bot.remove_plugin(info_plugin)
