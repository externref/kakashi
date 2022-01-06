from aiosqlite import connect
from disnake.colour import Color
from disnake.ext.commands.core import command

colors = {
    "red": Color.red(),
    "blue": Color.blue(),
    "yellow": Color.yellow(),
    "purple": Color.purple(),
    "darkblue": Color.dark_blue(),
    "white": 0xFFFFFF,
    "black": 0x000000,
    "pink": 0xFFC0CB,
    "cyan": 0x00FFFF,
    "skyblue": 0x87CEEB,
    "green": Color.green(),
}


class Parser:
    async def command_signature(command):
        command_signature = ""
        for arg in command.signature.split("] ["):
            if "=" in arg:
                parsed_arg = "{" + arg.split("=")[0].strip("[]<>]") + "}"
            else:
                parsed_arg = "[" + arg.strip("[]<>") + "]"
                if parsed_arg == "[]":
                    parsed_arg = ""
            command_signature += parsed_arg + " "

        return command_signature


class EmbedColor:
    async def color_for(guild):
        if not guild:
            color = await EmbedColor.get_embed_color(0)
        else:
            color = await EmbedColor.get_embed_color(str(guild.id))
        return colors[color]

    async def get_embed_color(guild_id: str):
        async with connect("database/guild.db") as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    """
                    SELECT * FROM colors
                    WHERE guild_id = ?
                    """,
                    (str(guild_id),),
                )
                guild_data = await data.fetchone()
                if guild_data:
                    return guild_data[1]
                else:
                    return "blue"
