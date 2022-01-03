from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.context import Context
from disnake.ext.commands.core import command, bot_has_permissions, has_permissions
from disnake.member import Member
from disnake.role import Role
from disnake.embeds import Embed
from kakashi.core.exts import EmbedColor


class Utilities(Cog, name="utility"):
    """
    Utilities for your server
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = "🛠️"
        self.banner = "https://cdn.discordapp.com/emojis/920959102065188894.png"
        self.help_desc = "Manage your server with these utility tools !"
        super().__init__()

    @command(
        name="addrole",
        aliases=["+role"],
        description="Adding a role to the mentioned user",
    )
    @has_permissions(manage_roles=True)
    @bot_has_permissions(
        manage_roles=True,
        send_messages=True,
        embed_links=True,
        read_message_history=True,
    )
    async def add_role_to_user(self, ctx: Context, member: Member, role: Role):
        """
        Adding a role to a user
        """
        if ctx.author.top_role.position <= role.position:
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["cross"]} Nuuu , you can\'t add that role to a user',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
            return
        try:
            await member.add_roles(role, reason=f"Added by {ctx.author}")
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["tick"]}Gave the `{role.name}` role to `{member.name}`',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
        except:
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["cross"]}I was unable to add that role\nThis can be because the role cannot be added to a user manually or the bot does not have enough hierachy to do that',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )

    @command(
        name="permissions",
        aliases=["permson", "checkperms"],
        description="Displays all the permissions on a user (server specific)",
    )
    @has_permissions(manage_roles=True)
    @bot_has_permissions(
        send_messages=True, embed_links=True, read_message_history=True
    )
    async def send_permissions(self, ctx: Context, member: Member = None):
        """
        Check member's Permissions
        """
        member = member or ctx.author
        perms = [perm[0] for perm in member.guild_permissions if perm[1]]
        if not perms:
            return await ctx.reply(
                embed=Embed(
                    description=f"No perms found on the member `{member.name}`",
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
        await ctx.reply(
            embed=Embed(
                description=(" , ".join(perms)).replace("_", " ").title(),
                color=await EmbedColor.color_for(ctx.guild),
            )
        )

    @command(name="removerole", aliases=["-role"])
    @has_permissions(manage_roles=True)
    @bot_has_permissions(
        send_messages=True, embed_links=True, read_message_history=True
    )
    async def remove_role_from_user(self, ctx: Context, member: Member, role: Role):
        """
        Removing a role from a user
        """
        if ctx.author.top_role.position <= role.position:
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["cross"]} Nuuu , you can\'t remove that role from a user',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
            return
        try:
            await member.add_roles(role, reason=f"Removed by {ctx.author}")
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["tick"]} Removed the `{role.name}` role from `{member.name}`',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
        except:
            await ctx.reply(
                embed=Embed(
                    description=f'{ctx.bot.my_emojis["cross"]}I was unable to remove that role\nThis can be because the role cannot be added to a user manually or the bot does not have enough hierachy to do that',
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )


def setup(bot: Bot):
    bot.add_cog(Utilities(bot))
