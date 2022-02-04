from typing import Union

from hikari.guilds import Guild
from hikari.colors import Color, Colorish

from lightbulb.app import BotApp
from lightbulb.context.base import Context


class ColorImpl:
    def __init__(self) -> None:
        self.color_dict = {
            "red": Color(0xFF0000),
            "blue": Color(0x0000FF),
            "cyan": Color(0x00FFFF),
            "orange": Color(0xFFA500),
            "yellow": Color(0xFFFF00),
            "purple": Color(0x800080),
            "pink": Color(0xFFFF00),
            "gray": Color(0x808080),
            "green": Color(0x00FF00),
            "gold": Color(0xFFD700),
            "lime": Color(0x00FF00),
            "black": Color(0x000000),
            "skyblue": Color(0x87CEEB),
            "snow": Color(0xFFFAFA),
            "white": Color(0xFFFFFF),
        }
        self.color_cache = {}

    async def color_for_current(
        self, obj: Union[Context, Guild], bot: BotApp
    ) -> Colorish:
        if isinstance(obj, Guild):
            guild_id = obj.id
        elif isinstance(obj, Context):
            guild_id = obj.guild_id
        cached_color = self.color_cache.get(str(guild_id))
        if cached_color:
            return cached_color
        async with bot.guild_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM colors
                WHERE guild_id = ?
                """,
                (str(guild_id),),
            )
            data = await cursor.fetchone()
        if not data:
            self.color_cache[str(guild_id)] = self.color_dict["snow"]
            return self.color_dict["snow"]
        else:
            self.color_cache[str(guild_id)] = self.color_dict[data[1]]
            return self.color_dict[data[1]]

    async def insert_color_for_guild(self, context: Context, color: str) -> None:
        async with context.bot.guild_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM colors
                WHERE guild_id = ?
                """,
                (str(context.guild_id),),
            )
            data = await cursor.fetchone()
            if data:
                await cursor.execute(
                    """
                    UPDATE colors
                    SET color = ?
                    WHERE guild_id = ?
                    """,
                    (color, str(context.guild_id)),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO colors
                    (guild_id , color)
                    VALUES ( ? , ? )
                    """,
                    (str(context.guild_id), color),
                )
            self.color_cache[str(context.guild_id)] = self.color_dict[color]
            await context.bot.guild_database.commit()

    @property
    def blue(self) -> Colorish:
        return Color(0x0000FF)

    @property
    def red(self) -> Colorish:
        return Color(0xFF0000)

    @property
    def cyan(self) -> Colorish:
        return Color(0x00FFFF)

    @property
    def green(self) -> Colorish:
        return Color(0x00FF00)

    @property
    def purple(self) -> Colorish:
        return Color(0x800080)

    @property
    def yellow(self) -> Colorish:
        return Color(0xFFFF00)

    @property
    def pink(self) -> Colorish:
        return Color(0xFFC0CB)


ColorHelper = ColorImpl()
