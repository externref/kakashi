from hikari.guilds import Role
from hikari.embeds import Embed
from hikari.guilds import Member

from lightbulb.context import Context

from .hex import ColorHelper


class InfoEmbedImpl:
    """
    Class helping for bot's info commands
    """

    async def embed_for_member(self, ctx: Context, member: Member):
        perms = []
        for role in member.get_roles():
            perms += role.permissions
        embed = Embed(color=ColorHelper.pink)
        info_dict = {
            "Name in Server ": member.display_name,
            "User ID": int(member.id),
            "Account Created": f'<t:{int(member.created_at.timestamp())}:R> `{member.created_at.strftime("%#d %B %Y")}`',
            "Member Joined": f'<t:{int(member.joined_at.timestamp())}:R> `{member.joined_at.strftime("%#d %B %Y")}`',
            "Top role of Member": member.get_top_role().mention,
            "Bot Account": str(member.is_bot)
            .replace("True", "Yes")
            .replace("False", "Nope"),
            "Roles on member": len(member.get_roles()) - 1,
        }
        embed.description = "\n".join(
            ("**" + str(key) + " :** " + str(info_dict[key]))
            for key in info_dict.keys()
        )
        embed.set_author(name=member.username)
        embed.set_footer(
            text=f"Requested by : {ctx.author}",
            icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
        )
        embed.set_thumbnail(member.avatar_url or member.default_avatar_url)
        embed.add_field(
            name="Permissions",
            value=await self.filter_perms(
                " , ".join([str(perm) for perm in perms]), ctx, member
            ),
        )
        return embed

    async def embed_for_role(self, ctx: Context, role: Role):
        embed = Embed(color=ColorHelper.red, title=f"{role.name} ROLE")
        info_dict = {
            "Role ID": role.id,
            "Mention": "`" + role.mention + "`",
            "Role Color": role.color,
            "Created on": f'<t:{int(role.created_at.timestamp())}:R> `{role.created_at.strftime("%#d %B %Y")}`',
            # TODO : 'Members with the role' : len([member for member in ctx.get_guild().get_members() if role in ctx.get_guild().get_member(member.id).get_roles()]),
            "Hoisted": role.is_hoisted,
            "Mentionable": role.is_mentionable,
            "Perms on Role ": await self.filter_perms(
                " , ".join([perm.name for perm in role.permissions]), ctx
            ),
        }
        embed.description = "\n".join(
            ("**" + str(key) + " :** " + str(info_dict[key]))
            for key in info_dict.keys()
        )
        embed.set_footer(
            text=f"Requested by : {ctx.author}",
            icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
        )
        return embed

    async def filter_perms(self, perm_str: str, ctx: Context, member: Member = None):
        permissions = (
            (
                perm_str.replace(", ADD_REACTIONS", "")
                .replace(", CONNECT", "")
                .replace(", CREATE_INSTANT_INVITE", "")
                .replace(", READ_MESSAGE_HISTORY", "")
                .replace(", REQUEST_TO_SPEAK", "")
                .replace(", SPEAK", "")
                .replace(", USE_APPLICATION_COMMANDS", "")
                .replace(", USE_EXTERNAL_EMOJIS", "")
                .replace(", VIEW_CHANNELS", "")
                .replace(", VIEW_CHANNEL", "")
                .replace(", CHANGE_NICKNAME", "")
                .replace(", SEND_MESSAGES", "")
                .replace(", USE_VOICE_ACTIVITY", "")
            )
            .replace("GUILD", "SERVER")
            .title()
            .replace("_", " ")
        )

        if "Administrator" in permissions:
            permissions = "Server Administrator"
        if member and member.id == ctx.get_guild().owner_id:
            permissions = "Server Owner"
        if not permissions:
            permissions = "No Special Perms"

        return permissions


InfoEmbedHelper = InfoEmbedImpl()
