from functools import cache
import sqlite3

from lightbulb.app import BotApp
from lightbulb.context import Context

from hikari.messages import Message
from hikari.events import GuildMessageDeleteEvent, GuildBulkMessageDeleteEvent

from typing import Union


def initialise_databases() -> None:
    """CREATING THE DATABASE FILES AND TABLES IN CASE THEY DONT EXIST ALREADY"""
    conn = sqlite3.connect("database/guilds.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prefixes
        ( guild_id TEXT , prefix TEXT )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS colors
        (guild_id TEXT , color TEXT )
        """
    )
    conn.commit()
    conn.close()
    conn = sqlite3.connect("database/automations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messagelogs
        ( guild_id TEXT , channel_id TEXT )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS welcomer 
        ( guild_id TEXT , channel_id TEXT , message TEXT , color TEXT , welcome_type TEXT)
        """
    )
    conn.commit()
    conn.close()


class PrefixHandlerImpl:
    """Used to handle prefixes!"""

    def __init__(self) -> None:
        self.prefix_cache = {}

    async def prefix_with_ctx(self, ctx: Context) -> str:
        cached_prefix = self.prefix_cache.get(str(ctx.guild_id))
        if cached_prefix:
            return cached_prefix
        async with ctx.bot.guild_database.cursor() as cursor:
            await cursor.execute(
                """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """,
                (ctx.guild_id,),
            )
            data = await cursor.fetchone()
        if data:
            self.prefix_cache[str(ctx.guild_id)] = data[1]
            return data[1]
        else:
            self.prefix_cache[str(ctx.guild_id)] = "."
            return "."

    async def prefix_setter(self, ctx: Context, new_prefix: str) -> None:
        async with ctx.bot.guild_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM prefixes
                WHERE guild_id = ?
                """,
                (str(ctx.guild_id),),
            )
            if await cursor.fetchone():
                await cursor.execute(
                    """
                    UPDATE prefixes
                    SET prefix = ?
                    WHERE guild_id = ?
                    """,
                    (
                        new_prefix,
                        str(ctx.guild_id),
                    ),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO prefixes
                    ( guild_id , prefix )
                    VALUES (? , ?)
                    """,
                    (
                        str(ctx.guild_id),
                        new_prefix,
                    ),
                )
            self.prefix_cache[str(ctx.guild_id)] = new_prefix
            return await ctx.bot.guild_database.commit()

    async def prefix_getter(self, bot: BotApp, message: Message) -> str:
        cached_prefix = self.prefix_cache.get(str(message.guild_id))
        if cached_prefix:
            return cached_prefix
        async with bot.guild_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM prefixes
                WHERE guild_id = ?
                """,
                (message.guild_id,),
            )
            data = await cursor.fetchone()
        if data:
            self.prefix_cache[str(message.guild_id)] = data[1]
            return data[1]
        else:
            self.prefix_cache[str(message.guild_id)] = "."
            return "."


class MessageLogDatabase:
    """Class Managing Message Logs Database"""

    async def get_data(
        ctx: Union[Context, GuildMessageDeleteEvent, GuildBulkMessageDeleteEvent],
        bot: BotApp,
    ):
        async with bot.automation_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM messagelogs
                WHERE guild_id = ?
                """,
                (str(ctx.guild_id),),
            )
            data = await cursor.fetchone()
        if data:
            return data[1]

    async def insert_data(ctx: Context, channel_id: int):
        async with ctx.bot.automation_database.cursor() as cursor:
            pre_existing = await MessageLogDatabase.get_data(ctx)
            if pre_existing:
                await cursor.execute(
                    """
                    UPDATE messagelogs
                    SET channel_id = ?
                    WHERE guild_id = ?
                    """,
                    (str(channel_id), str(ctx.guild_id)),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO messagelogs
                    ( guild_id , channel_id )
                    VALUES ( ? , ? )
                    """,
                    (str(ctx.guild_id), str(channel_id)),
                )
            await ctx.bot.automation_database.commit()


class WelcomeDB:
    async def get_guild_data(bot: BotApp, guild_id: str):
        async with bot.guild_database.cursor() as cursor:
            data = await cursor.execute(
                """
                    SELECT * FROM welcomer 
                    WHERE guild_id = ?
                    """,
                (str(guild_id),),
            )
            guild_data = await data.fetchone()
            if not guild_data:
                return
            return guild_data

    async def update_or_insert_guild_data(
        bot: BotApp,
        guild_id: str,
        channel_id: str,
        message: str,
        color: str = "blue",
        type: str = "embedmessage",
    ) -> None:
        async with bot.guild_database.cursor() as cursor:
            data = await cursor.execute(
                """
                    SELECT * FROM welcomer 
                    WHERE guild_id = ?
                    """,
                (str(guild_id),),
            )
            is_data = await data.fetchone()
            if is_data:
                await cursor.execute(
                    """
                        UPDATE welcomer
                        SET channel_id = ? , message = ? , color = ? , welcome_type = ?
                        where guild_id = ?
                        """,
                    (
                        str(channel_id),
                        str(message),
                        str(color),
                        str(type),
                        str(guild_id),
                    ),
                )
                await bot.guild_database.commit()
            else:
                await cursor.execute(
                    """
                        INSERT INTO welcomer
                        ( guild_id , channel_id , message , color , welcome_type )
                        VALUES ( ? , ? , ? , ? , ?)
                        """,
                    (
                        str(guild_id),
                        str(channel_id),
                        message,
                        color,
                        type,
                    ),
                )
                await bot.guild_database.commit()
            return


PrefixHandler = PrefixHandlerImpl()
