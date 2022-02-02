from typing import Optional

from lightbulb.app import BotApp
from lightbulb.plugins import Plugin

from hikari.embeds import Embed
from hikari.events import (
    GuildMessageDeleteEvent,
    GuildBulkMessageDeleteEvent,
    GuildMessageUpdateEvent,
)

from hikari.messages import Message
from hikari.errors import ForbiddenError

from kakashi.helpers.db_handler import MessageLogDatabase

event_listeners = Plugin(name="Events", description="An Listener Plugin")


@event_listeners.listener(GuildMessageDeleteEvent)
async def log_deleted_message(event: GuildMessageDeleteEvent) -> None:
    data = await MessageLogDatabase.get_data(event, event_listeners.bot)
    if not data:
        return
    log_channel = event.get_guild().get_channel(int(data))
    if not log_channel:
        return
    if not event.old_message.content:
        return
    embed = (
        Embed(description=event.old_message.content, color=0xFFFFFF)
        .set_author(
            name=str(event.old_message.author),
            icon=event.old_message.author.avatar_url
            or event.old_message.author.default_avatar_url,
        )
        .add_field(name="Message ID", value=event.message_id, inline=True)
        .add_field(name="Channel", value=f"<#{event.channel_id}>", inline=True)
    )
    try:
        await log_channel.send(embed=embed)
    except ForbiddenError:
        return


@event_listeners.listener(GuildBulkMessageDeleteEvent)
async def log_bulk_deleted_message(event: GuildBulkMessageDeleteEvent) -> None:
    data = await MessageLogDatabase.get_data(event, event_listeners.bot)
    if not data:
        return
    log_channel = event.get_guild().get_channel(int(data))
    if not log_channel:
        return
    embed = Embed(
        color=0xFFFFFF,
        description=f"bulk Message Delete in <#{event.channel_id}>\n`{len(event.message_ids)}` messages deleted.",
    )
    try:
        await log_channel.send(embed=embed)
    except ForbiddenError:
        return


@event_listeners.listener(GuildMessageUpdateEvent)
async def log_edited_messages(event: GuildMessageUpdateEvent) -> None:
    if not event.old_message:
        return
    if event.message.content == event.old_message.content:
        return
    data = await MessageLogDatabase.get_data(event, event_listeners.bot)
    if not data:
        return
    log_channel = event.get_guild().get_channel(int(data))
    if not log_channel:
        return
    message_url = f"https://discord.com/channels/{event.old_message.guild_id}/{event.old_message.channel_id}/{event.old_message.id}"
    embed = (
        Embed(
            color=0xFFFFFF,
            description=f"[Jump to message]({message_url})\n**BEFORE** : {event.old_message.content[:2000]}\n**AFTER** : {event.message.content[:2000]} ",
        )
        .set_author(
            name=str(event.old_message.author),
            icon=event.old_message.author.avatar_url
            or event.old_message.author.default_avatar_url,
        )
        .add_field(name="Message ID", value=event.message_id, inline=True)
        .add_field(name="Channel", value=f"<#{event.channel_id}>", inline=True)
    )
    try:
        await log_channel.send(embed=embed)
    except ForbiddenError:
        return


def load(bot: BotApp) -> None:
    bot.add_plugin(event_listeners)


def unload(bot: BotApp) -> None:
    bot.remove_plugin(event_listeners)
