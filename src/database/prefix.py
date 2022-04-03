import sqlite3
from typing import Union

import aiosqlite

from hikari.guilds import Guild
from hikari.messages import Message

from lightbulb.app import BotApp
from lightbulb.context import Context


class PrefixHandler:
    def __init__(self, default_prefix: str, database_file: str = "prefixes.db") -> None:
        self.default_prefix = default_prefix
        self.database_file = database_file
        self.prefix_cache = {}
        self.connection_state = False
        self.create_database_task(database_file)

    def create_database_task(self, filename: str) -> None:
        """Initialising the sqlite database and creating a table in it"""
        if not filename.lower().endswith(".db"):
            raise BaseException(
                "The database_file should be a file with `.db` extensions !"
            )
        with sqlite3.connect(filename) as database:
            cursor = database.cursor()
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS  prefixes
                    (guild_id TEXT , prefix TEXT)
                    """
            )
            database.commit()

    async def create_connection(self) -> None:
        """The internals call it for making a connection to the database"""
        self.database_connection = await aiosqlite.connect(self.database_file)

    async def get_prefix(self, bot: BotApp, message: Message) -> str:
        """Method to use for the `prefix` arg in the lightbulb.BotApp object."""
        if not self.connection_state:
            await self.create_connection()

        prefix_str = (
            self._from_cache(message)
            or await self._from_database(message)
            or self.default_prefix
        )
        return prefix_str

    def _from_cache(self, message: Message) -> str:
        """Getting data from prefix_cache dictionary"""
        return self.prefix_cache.get(str(message.guild_id))

    async def _from_database(self, obj: Union[Message, Guild]) -> str:
        """Fetching the database from the sqlite3 database"""
        if isinstance(obj, Message):
            guild_id = obj.guild_id
        elif isinstance(obj, Guild):
            guild_id = obj.id
        async with self.database_connection.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM prefixes 
                WHERE guild_id = ?
                """,
                (str(guild_id),),
            )
            guild_data = await cursor.fetchone()
        if guild_data:
            self.prefix_cache[str(guild_id)] = guild_data[1]
            return guild_data[1]
        else:
            self.prefix_cache[str(guild_id)] = self.default_prefix
            return

    async def set_prefix(self, ctx: Context, new_prefix: str) -> None:
        """Adding/Updating prefix for a server."""
        guild = ctx.get_guild()
        guild_data = await self._from_database(guild)
        print(guild_data)
        async with self.database_connection.cursor() as cursor:
            if guild_data:
                await cursor.execute(
                    """
                UPDATE prefixes
                SET prefix = ?
                WHERE guild_id = ?
                """,
                    (new_prefix, str(guild.id)),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO prefixes
                    (guild_id , prefix)
                    VALUES (? , ? )
                    """,
                    (str(guild.id), new_prefix),
                )
            await self.database_connection.commit()
            self.prefix_cache[str(guild.id)] = new_prefix
