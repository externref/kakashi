import aiosqlite

from lightbulb.context.base import Context

from hikari.messages import Message
from hikari.channels import TextableGuildChannel


class WelcomerHandler:
    connection: aiosqlite.Connection
    DEFAULT_WELCOME_MESSAGE = "$user, Welcome to $server"

    async def setup(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect("welcome.db")
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS welcome
                (guild_id TEXT, channel_id TEXT, message TEXT, hex_code TEXT)
                """
            )
        await conn.commit()
        self.connection = conn

    async def insert_data(self, guild_id: int, channel_id: int, hex_code: str) -> None:
        cursor = await self.connection.cursor()
        await cursor.execute(
            """
            INSERT INTO welcome
            ( guild_id, channel_id, message, hex_code )
            VALUES ( ?, ?, ?,? )
            """,
            (str(guild_id), str(channel_id), self.DEFAULT_WELCOME_MESSAGE, hex_code),
        )
        await self.connection.commit()

    async def update_data(self, channel_id: int)-> None:
        ...
