from . import (
    Bot , 
    Cog ,
    Context 
)
from disnake.ext.commands import command , has_permissions , bot_has_permissions , guild_only , slash_command
from disnake import User , Embed , Member , ApplicationCommandInteraction , Option , OptionType
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
        name='userinfo',
        aliases=['whois','ui'],
        description='Info about a guild Member including Joined date , ID , roles and more'
    )
    @guild_only()
    @bot_has_permissions(send_messages=True , embed_links=True , read_message_history=True)
    async def send_userinfo(self , ctx : Context , member : Member = None):
        """
        Info about mentioned member
        """
        member = member or ctx.author
        await ctx.reply(
            embed= await EmbedMaker.for_user(ctx , member)
        )
    
    @command(
        name='serverinfo',
        aliases=['si' , 'svinfo']
    )
    @guild_only()
    async def guild_info(self , ctx: Context):
        pass
    

    

def setup(bot : Bot):
    bot.add_cog(Info(bot))

class EmbedMaker:
    async def for_user(ctx : Union[Context ,  ApplicationCommandInteraction], member : Member):
        position = len([m for m in ctx.guild.members if member.joined_at > m.joined_at])
        roles = " , ".join((role.mention for role in member.roles[1:][::-1]))
        info_dict = {
            'Display Name' : member.display_name,
            'ID' : member.id,
            'Joined Server' : f"{member.joined_at.strftime('%d %B %Y')}` <t:{int(member.joined_at.timestamp())}:R> `{position}/{ctx.guild.member_count}",
            'Joined Discord' : f"{member.created_at.strftime('%d %B %Y')}` <t:{int(member.created_at.timestamp())}:R> `<-",
            'User is Bot' : member.bot,
            'Status' : member.status ,
            'Top Role' : member.top_role,
            'Member Color': member.color 
        }
        info_data = "\n".join(("**"+str(key)+"** : "+"`"+str(info_dict[key])+"`") for key in info_dict.keys())
        embed = (Embed(
            color = await EmbedColor.color_for(ctx.guild),
            description=f'{info_data}\n**ROLES** : {roles or "No roles"}'
        )
        .set_thumbnail(url=member.display_avatar).set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        .set_author(name=member , icon_url=member.display_avatar)
        )
        return embed
    
    async def for_guild(ctx : Union[Context ,  ApplicationCommandInteraction]):
        pass