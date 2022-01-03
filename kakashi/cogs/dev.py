from disnake.embeds import Embed
from disnake.activity import Activity, ActivityType
from disnake.enums import Status
from disnake.guild import Guild
from disnake.colour import Color
from disnake.ext.tasks import loop
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.context import Context
from disnake.ext.commands.core import (
    command,
    is_owner,
    MemberNotFound,
    UserNotFound,
    RoleNotFound,
    MissingPermissions,
    BotMissingPermissions,
    NotOwner,
    CommandOnCooldown,
    CommandError,
    BadUnionArgument,
    MissingRequiredArgument,
    CommandNotFound,
    PrivateMessageOnly,
    NoPrivateMessage,
)
from kakashi.core.exts import EmbedColor
from os import getenv, environ


class Developer(Cog, name="botbase"):
    def __init__(self, bot: Bot):
        environ["JISHAKU_EMBEDDED_JSK"] = "true"
        self.bot = bot

    @Cog.listener("on_ready")
    async def when_bot_ready(self):
        await self.start_status_task()

    @loop(seconds=30)
    async def status_task(self):
        mc = 0
        mc_list = [guild.member_count for guild in self.bot.guilds]
        for count in mc_list:
            mc += count
        await self.bot.change_presence(
            activity=Activity(
                type=ActivityType.listening,
                name=f"{len(self.bot.guilds)} servers with {mc} members",
            ),
            status=Status.idle,
        )

    async def start_status_task(self):
        await self.bot.wait_until_ready()
        self.status_task.start()

    @command(name="refresh", aliases=["reboot"])
    @is_owner()
    async def owner_reload_cogs(self, ctx: Context):
        for cog in self.bot.cog_list[1:]:
            try:
                self.bot.reload_extension("kakashi.cogs." + cog)
                print(cog, "loaded")
            except Exception as e:
                raise e
        await ctx.reply(
            "Reloaded `"
            + "` , `".join(cog + ".py" for cog in self.bot.cog_list)
            + "` files"
        )

    @Cog.listener("on_guild_join")
    async def added_to_server(self, guild: Guild):
        bots = [member for member in guild.members if member.bot]
        embed = Embed(color=Color.green())
        embed.add_field(name="Name", value=guild.name, inline=False)
        embed.add_field(name="Owner", value=guild.owner or guild.owner_id, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(
            name="Member | Bots",
            value=str(guild.member_count) + " | " + str(len(bots)),
            inline=False,
        )
        embed.add_field(
            name="Current Server Count", value=len(self.bot.guilds), inline=False
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await self.bot.get_channel(int(getenv("LOG_CHANNEL"))).send(embed=embed)

    @Cog.listener("on_guild_remove")
    async def removed_from_server(self, guild: Guild):
        bots = [member for member in guild.members if member.bot]
        embed = Embed(color=Color.red())
        embed.add_field(name="Name", value=guild.name, inline=False)
        embed.add_field(name="Owner", value=guild.owner or guild.owner_id, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(
            name="Member | Bots",
            value=str(guild.member_count) + " | " + str(len(bots)),
            inline=False,
        )
        embed.add_field(
            name="Current Server Count", value=len(self.bot.guilds), inline=False
        )
        await self.bot.get_channel(int(getenv("LOG_CHANNEL"))).send(embed=embed)

    @Cog.listener("on_command_error")
    async def error_handler(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, NotOwner):
            description, emoji = (
                f"`{ctx.command.name}` is an owner only command",
                self.bot.my_emojis["cross"],
            )
        elif isinstance(error, MissingPermissions):
            description, emoji = (
                f"You need `{'` , `'.join(error.missing_permissions).replace('guild','server')}` permission(s) to run this command",
                self.bot.my_emojis["cross"],
            )
        elif isinstance(error, BotMissingPermissions):
            return await ctx.send(
                "Bot requires `{'` , `'.join(error.missing_permissions).replace('guild','server')}` permission(s) to run this command"
            )
        elif isinstance(error, RoleNotFound):
            (
                description,
                emoji,
            ) = f"Role `{error.argument}` was not found", self.bot.get_emoji(
                888098945883050065
            )
        elif isinstance(error, MemberNotFound):
            (
                description,
                emoji,
            ) = f"Member `{error.argument}` was not found", self.bot.get_emoji(
                888098801326383104
            )
        elif isinstance(error, UserNotFound):
            (
                description,
                emoji,
            ) = f"User `{error.argument}` was not found", self.bot.get_emoji(
                888098801326383104
            )
        elif isinstance(error, BadUnionArgument):
            description, emoji = (
                f"Invalid {error.param.name} supplied",
                self.bot.my_emojis["cross"],
            )
        elif isinstance(error, CommandOnCooldown):
            description, emoji = (
                f"You need to wait for {int(error.retry_after)} seconds before trying again",
                self.bot.get_emoji(841711427052240927),
            )
        elif isinstance(error, MissingRequiredArgument):
            description, emoji = f"`{error.param.name}` is a required argument", "❗"
        elif isinstance(error, NoPrivateMessage):
            description, emoji = (
                f"`{ctx.command.name}` works only in servers",
                self.bot.my_emojis["cross"],
            )
        elif isinstance(error, PrivateMessageOnly):
            description, emoji = (
                f"`{ctx.command.name}` works in dms only",
                self.bot.my_emojis["cross"],
            )
        else:
            raise error
        embed = Embed(
            description=str(emoji) + " " + description,
            color=await EmbedColor.color_for(ctx.guild),
        )
        await ctx.reply(embed=embed, delete_after=10)


def setup(bot: Bot):
    bot.add_cog(Developer(bot))
