from . import (
    Bot , 
    Cog ,
    Context 
)
from disnake.ext.commands import command , has_permissions , bot_has_permissions , guild_only 
from disnake import User , Embed , Member , Role , ApplicationCommandInteraction 
from typing import Union
from datetime import datetime
from exts import EmbedColor

class Info(Cog , name='info'):
    def __init__(self , bot: Bot):
        self.bot = bot
        self.emoji = ""
    
    @command(
        name='avatar',
        aliases=['av','pfp'],
        description= 'User\'s avatar enlarged , author\'s if no user is mentioned'
    )
    @bot_has_permissions(send_messages=True , embed_links=True , read_message_history=True)
    async def send_avatar(self , ctx : Context , user : User = None):
        """
        User's Avatar
        """
        user = user or ctx.author
        animated = 'Static'
        if user.avatar and user.avatar.is_animated():
            animated = 'Animated'
        await ctx.reply(
            embed = Embed(
                timestamp=datetime.now(),
                description=f'[Download]({(user.avatar or user.default_avatar).url}) | Type : {animated}',
                color = await EmbedColor.color_for(ctx.guild)
            ).set_image(url=(user.avatar or user.default_avatar).url).set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar).set_author(name=f'{user}\' AVATAR')
        )
    
    @command(
        name='info',
        aliases=['information'],
        description=f'Get infomation about mentioned object , can be a user / role'
    )
    @guild_only()
    @bot_has_permissions(send_messages=True , embed_links=True , read_message_history=True)
    async def get_information_about(self , ctx : Context , target : Union[Member , Role]):
        """
        
        """
        if isinstance(target ,  Member) : embed = await EmbedMaker.for_member(ctx , target)
        elif isinstance(target , Role) : embed = await EmbedMaker.for_role(ctx , target)
        await ctx.reply(embed=embed)

    @command(
        name='userinfo',
        aliases=['whois','ui'],
        description='Info about a server Member including Joined date , ID , roles and more'
    )
    @guild_only()
    @bot_has_permissions(send_messages=True , embed_links=True , read_message_history=True)
    async def send_userinfo(self , ctx : Context , member : Member = None):
        """
        Info about mentioned member
        """
        member = member or ctx.author
        await ctx.reply(
            embed= await EmbedMaker.for_member(ctx , member)
        )
    
    
    @command(
        name='roleinfo',
        aliases=['ri'],
        description='Info about a Role including Created date , ID , memebrs with role and more'
    )
    async def send_roleinfo(self , ctx : Context , role : Role) :
        """
        Info about a role
        """
        await ctx.reply(
            embed =await EmbedMaker.for_role(ctx , role)
        )
    @command(
        name='serverinfo',
        aliases=['si' , 'svinfo']
    )
    @guild_only()
    @bot_has_permissions(send_messages=True , embed_links=True , read_message_history=True)
    async def guild_info(self , ctx: Context):
        """
        Info about the Server
        """
        await ctx.reply(
            embed= await EmbedMaker.for_guild(ctx)
        )
        
def setup(bot : Bot):
    bot.add_cog(Info(bot))

class EmbedMaker:
    async def for_member(ctx : Union[Context ,  ApplicationCommandInteraction], member : Member) -> Embed:
        position = len([m for m in ctx.guild.members if member.joined_at > m.joined_at])
        roles = " , ".join((role.mention for role in member.roles[1:][::-1]))
        info_dict = {
            'Display Name' : member.display_name,
            'ID' : member.id,
            'Joined Server' : f"{member.joined_at.strftime('%d %B %Y')}` <t:{int(member.joined_at.timestamp())}:R> `{position+1}/{ctx.guild.member_count}",
            'Joined Discord' : f"{member.created_at.strftime('%d %B %Y')}` <t:{int(member.created_at.timestamp())}:R> `<-",
            'User is Bot' : member.bot,
            'Status' : member.status ,
            'Top Role' : member.top_role,
            'Member Color': member.color 
        }
        info_data = "\n".join(("**"+str(key)+" :** "+"`"+str(info_dict[key])+"`") for key in info_dict.keys())
        embed = (Embed(
            color = await EmbedColor.color_for(ctx.guild),
            description=f'{info_data}\n**ROLES** : {roles or "No roles"}'
        )
        .set_thumbnail(url=member.display_avatar).set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        .set_author(name=member , icon_url=member.display_avatar)
        )
        return embed

    async def for_role(ctx :Union[Context ,  ApplicationCommandInteraction] , role : Role) -> Embed:
        info_dict = {
            'Name' : role.name,
            'ID' : role.id,
            'Created On' : f"{role.created_at.strftime('%d %B %Y')}` <t:{int(role.created_at.timestamp())}:R> `<-",
            'Role Color' : role.color ,
            'Members with the role': len(role.members),
            'Hosited' : role.hoist,
            'Pingable' : role.mentionable,
        }
        if ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild: info_dict['Perms']= " , ".join(permission[0] for permission in role.permissions if permission[1])
        members = ' , '.join(member.mention for member in role.members[:20])
        desc = "\n".join(("**"+str(key)+" :** "+"`"+str(info_dict[key])+"`") for key in info_dict.keys()) +"\n**MEMBERS :**"+members
        embed = Embed(
            description=desc ,
            color = await EmbedColor.color_for(ctx.guild)
        ).set_author(name=f"Info about {role.name} role")
        embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        return embed

    async def for_guild(ctx : Union[Context ,  ApplicationCommandInteraction]) -> Embed:
        info_dict = {
            'Owner' : f"`{ctx.guild.owner}`" or f"<@{ctx.guild.owner_id}>",
            "ID" : ctx.guild.id,
            'Created On' : f"{ctx.guild.created_at.strftime('%d %B %Y')}` <t:{int(ctx.guild.created_at.timestamp())}:R> `<-",
            'Region' : ctx.guild.region or "Not Specific",
            'Members' : ctx.guild.member_count,
            'Roles in the server' : len(ctx.guild.roles),
            'Booster Role': ctx.guild.premium_subscriber_role or 'No role',
            'Boosters | Boost Level' : " | ".join([str(ctx.guild.premium_subscription_count),str(ctx.guild.premium_tier)])
        }
        if ctx.guild.icon : url = ctx.guild.icon.url
        else : url= Embed.Empty
        info_data = "\n".join(("**"+str(key)+" :** "+"`"+str(info_dict[key])+"`") for key in info_dict.keys())
        embed = Embed(
            color = await EmbedColor.color_for(ctx.guild),
            description=info_data
        ).set_author(name=ctx.guild.name,icon_url=url )
        embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        if ctx.guild.icon : embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner : embed.set_thumbnail(url=ctx.guild.banner.url)
        return embed   


