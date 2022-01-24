import sqlite3
from hikari.messages import Message
from lightbulb.app import BotApp
from lightbulb.context import Context


def initialise_databases() -> None:
    conn = sqlite3.connect("database/guilds.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prefixes
        (guild_id TEXT , prefix TEXT )
        """
    )
    conn.commit()
    conn.close()
    conn = sqlite3.connect("database/reactionroles.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rr_roles
        (channel_id TEXT , message_id TEXT , reaction TEXT , role_id TEXT )
        """
    )
    conn.commit()
    conn.close()


class PrefixHandler:
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
            return "w!"

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
            return "w!"
