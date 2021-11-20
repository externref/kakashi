from typing import Optional, Union
from disnake.app_commands import Option
from disnake.enums import OptionType
from . import (
    Cog ,
    Context ,
    Bot
)
from disnake.ext.commands import command , has_permissions , bot_has_permissions , slash_command
from disnake import Member , Role , Embed , Color, user

class Utilities(Cog):
    def __init__(self , bot:Bot):
        self.bot = bot
        super().__init__()

    @command(
        name = 'addrole' , 
        aliases=['+role'] ,
        description = 'Adding a role to the mentioned user'
    )
    @has_permissions(manage_roles = True )
    @bot_has_permissions(manage_roles = True , send_messages=True , embed_links=True , read_message_history=True)
    async def add_role_to_user(self , ctx :Context, member : Member , role : Role):
        '''
        Adding a role to a user
        '''
        if ctx.author.top_role.position <= role.position:
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["cross"]} Nuuu , you can\'t add that role to a user',
                    color = Color.red()
                )
            )
            return
        try :
            await member.add_roles(role , reason = f'Added by {ctx.author}')
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["tick"]}Gave the `{role.name}` role to `{member.name}`',
                    color = Color.green()
                )
            )
        except:
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["cross"]}I was unable to add that role\nThis can be because the role cannot be added to a user manually or the bot does not have enough hierachy to do that',
                    color = Color.red()
                )
            )
    
    @command(
        name = 'permissions' ,
        aliases= ['permson' , 'checkperms'] 
    )
    @has_permissions(manage_roles = True)
    @bot_has_permissions(send_messages=True , embed_links = True  ,read_message_history=True)
    async def send_permissions(self , ctx : Context , member : Member = None):
        member = member or ctx.author
        perms = [perm[0] for perm in member.guild_permissions if perm[1]]
        if not perms :
            return await ctx.reply(
                embed = Embed(
                    description=f'No perms found on the member `{member.name}`',
                    color = Color.dark_blue()
                )
            )
        await ctx.reply(
            embed = Embed(
                description= (' , '.join(perms)).replace('_' , ' ').title(),
                color = Color.blue()
            )
        )

    @command(
        name = 'removerole',
        aliases=['-role']
    )
    @has_permissions(manage_roles = True)
    @bot_has_permissions(send_messages=True , embed_links = True  ,read_message_history=True)
    async def remove_role_from_user(self , ctx : Context , member : Member , role : Role):
        '''
        Removing a role from a user
        '''
        if ctx.author.top_role.position <= role.position:
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["cross"]} Nuuu , you can\'t remove that role from a user',
                    color = Color.red()
                )
            )
            return
        try :
            await member.add_roles(role , reason = f'Removed by {ctx.author}')
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["tick"]} Removed the `{role.name}` role from `{member.name}`',
                    color = Color.green()
                )
            )
        except:
            await ctx.reply(
                embed = Embed(
                    description=f'{ctx.bot.my_emojis["cross"]}I was unable to remove that role\nThis can be because the role cannot be added to a user manually or the bot does not have enough hierachy to do that',
                    color = Color.red()
                )
            )






def setup(bot : Bot):
    bot.load_extension(Utilities(bot))