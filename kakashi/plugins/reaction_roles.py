from lightbulb import commands
from lightbulb.context import Context
from lightbulb.app import BotApp
from lightbulb.plugins import Plugin
from lightbulb.commands.prefix import (
    PrefixCommand,
    PrefixCommandGroup,
    PrefixSubCommand,
)
from lightbulb.commands.slash import SlashCommand
from lightbulb.converters.special import EmojiConverter
from lightbulb.decorators import command, implements, add_checks, option
from hikari.channels import GuildTextChannel
from hikari.embeds import Embed
from hikari.guilds import Role
from hikari.emojis import UnicodeEmoji, CustomEmoji
from hikari.errors import NotFoundError
from typing import Union

from kakashi.exts.hex import ColorHelper

reaction_roles = Plugin(
    name="Reaction Roles", description="Reaction roles for role automation"
)


@reaction_roles.command
@command(
    name="reactionrole", aliases=["rr"], description="Reaction roles for your server"
)
@implements(PrefixCommandGroup)
async def rr_command(ctx: Context):
    """Make a reaction Role menu"""
    await ctx.bot.help_command.send_help(ctx, "rr")


@rr_command.child
@option(
    name="message_id",
    description="The ID of message on which reaction role is to be created ",
    required=True,
    type=int,
)
@option(
    name="emoji",
    description="The Emoji for the reaction role",
    required=True,
    type=EmojiConverter,
)
@option(
    name="role",
    description="The role to add on user upon reaction",
    required=True,
    type=Role,
)
@command(name="add", description="Add a new reaction role to a message")
@implements(PrefixSubCommand)
async def rr_add_command(ctx: Context):
    ch: GuildTextChannel = ctx.get_channel()
    try:
        msg = await ch.fetch_message(ctx.options.message_id)
    except NotFoundError:
        return await ctx.respond(
            embed=Embed(
                description=f"Any message with that ID was not found in {ch.mention}",
                color=ColorHelper.red,
            ),
            reply=True,
        )
    if isinstance(ctx.options.emoji, UnicodeEmoji):
        emoji_entry = ctx.options.emoji
    elif isinstance(ctx.options.emoji, CustomEmoji):
        emoji_entry = ctx.options.emoji.id


def load(bot: BotApp):
    bot.add_plugin(reaction_roles)
