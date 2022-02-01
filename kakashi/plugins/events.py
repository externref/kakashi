from hikari import MessageUpdateEvent
from lightbulb.plugins import Plugin
from lightbulb.app import BotApp
from hikari.embeds import Embed
from hikari.events import (
    GuildMessageDeleteEvent,
    GuildBulkMessageDeleteEvent,
    GuildMessageUpdateEvent,
)
from kakashi.exts.db_handler import MessageLogDatabase

event_listeners = Plugin(name="Events", description="An Listener Plugin")


@event_listeners.listener(GuildMessageDeleteEvent)
async def log_deleted_message(event: GuildMessageDeleteEvent):
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
    await log_channel.send(embed=embed)

@event_listeners.listener(GuildBulkMessageDeleteEvent)
async def log_bulk_deleted_message(event : GuildBulkMessageDeleteEvent):
    ...


@event_listeners.listener(GuildMessageUpdateEvent)
async def log_edited_messages(event: GuildMessageUpdateEvent):
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
    await log_channel.send(embed=embed)


def load(bot: BotApp):
    bot.add_plugin(event_listeners)
