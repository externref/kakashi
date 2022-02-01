import sqlite3
from hikari.messages import Message
from lightbulb.app import BotApp
from lightbulb.context import Context
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
    conn.commit()
    conn.close()


class PrefixHandler:
    """Used to handle prefixes!"""

    async def prefix_with_ctx(ctx: Context) -> str:
        async with ctx.bot.prefix_database.cursor() as cursor:
            await cursor.execute(
                """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """,
                (ctx.guild_id,),
            )
            data = await cursor.fetchone()
        if data:
            return data[1]
        else:
            return "."

    async def prefix_setter(ctx: Context, new_prefix: str) -> None:
        async with ctx.bot.prefix_database.cursor() as cursor:
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
            return await ctx.bot.prefix_database.commit()

    async def prefix_getter(bot: BotApp, message: Message) -> str:
        async with bot.prefix_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM prefixes
                WHERE guild_id = ?
                """,
                (message.guild_id,),
            )
            data = await cursor.fetchone()
        if data:
            return data[1]
        else:
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
