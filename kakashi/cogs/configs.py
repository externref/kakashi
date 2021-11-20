from disnake.ext.commands.core import has_permissions
from disnake.interactions.application_command import ApplicationCommandInteraction
from . import (
    Cog ,
    Button ,
    Bot ,
    Context , 
    View , 
)
from disnake.ext.commands import command , has_guild_permissions , bot_has_permissions , has_permissions ,slash_command
from aiosqlite3 import connect
from disnake import Embed ,Color, Option,OptionType
            
class Configurations(Cog):
    '''
    Bot Configurations for your server
    '''
    def __init__(self , bot : Bot):
        self.bot = bot

    @command(
        name = 'prefix' ,
        description ='Check the bot\'s prefix for the guild just in case you\'re lost'
    )
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True)
        
    async def send_prefix(self , ctx : Context):
        '''
        Send Bot's prefix for the guild 
        '''
        await ctx.reply(
            embed = Embed(
                color = Color.purple() ,
                description= f'{self.bot.my_emojis["wave"]} Prefix for **{ctx.guild.name}** is `{(await self.bot.get_prefix(ctx.message))[2]}`\nYou can also use my mention as prefix !'
            )
        )
        


    @command(
        name= 'prefix-set',
        aliases = ['set-prefix' , 'setprefix' , 'prefixset'],
        description = 'Change Bot\s prefix for a guild\nCannot include these characters : \` , `@` and `#`'
    )
    @has_guild_permissions(manage_guild = True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def change_prefix(self , ctx : Context, * , new_prefix : str):
        '''
        Change Bot\'s prefix for a guild
        '''
        if any([letter for letter in new_prefix if letter in ['@' , '`' , '#']]):
            return await ctx.reply(
                embed = Embed(
                    description=f"{ctx.bot.my_emojis['cross']} Bot prefix Cannot contain \` , `@` or `#` characters due to discord markdown .",
                    color = Color.red()
                )
            )
        await DataBaseHandler.insert_or_update_prefix(ctx , new_prefix)
        await ctx.reply(
            embed = Embed(
                description=f"{ctx.bot.my_emojis['tick']} Prefix has been set to `{new_prefix}` , You can always change the prefix with `prefix-set` command ",
                color= Color.green()
            )
        )
    
    @command(
        name= 'prefix-reset',
        aliases = ['prefix-clear']
    )
    @has_guild_permissions(manage_guild=True)
    @bot_has_permissions()
    async def remove_prefix_for_guild(self , ctx : Context):
        old_prefix = self.bot.get_prefix(ctx.message)
        await DataBaseHandler.insert_or_update_prefix(ctx , '.')
        await ctx.reply(
            embed = Embed(
                description=f'{self.bot.my_emojis["tick"]} Changed prefix back from `{old_prefix}` to `.`'
            )
        )

    @slash_command(
        name = 'prefix' ,
        description='Change prefix for the server',
        options = [
            Option(name='newprefix' , description='The new prefix for the server',type=OptionType.string , required=True)
        ]
    )
    async def change_prefix_slash(self , ctx : ApplicationCommandInteraction , newprefix : str):
        '''
        Change Bot\'s prefix for a guild
        '''
        if any([letter for letter in newprefix if letter in ['@' , '`' , '#']]):
            return await ctx.response.send_message(
                embed = Embed(
                    description=f"{ctx.bot.my_emojis['cross']} Bot prefix Cannot contain \` , `@` or `#` characters due to discord markdown .",
                    color = Color.red()
                )
            )
        await DataBaseHandler.insert_or_update_prefix(ctx , newprefix)
        await ctx.response.send_message(
            embed = Embed(
                description=f"{ctx.bot.my_emojis['tick']} Prefix has been set to `{newprefix}` , You can always change the prefix with `prefix-set` command ",
                color= Color.green()
            )
        )
        
        


class DataBaseHandler:
    async def get_prefix(ctx : Context):
        async with connect('database/prefixes.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    '''
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    ''' ,
                    (str(ctx.guild.id),)
                ) 
                prefix = data.fetchone()
                if not prefix :
                    return None 
                return prefix[1]

    async def insert_or_update_prefix(ctx : Context , new_prefix : str):
        async with connect('database/prefixes.db') as database:
            async with database.cursor() as cursor:
                if not await DataBaseHandler.get_prefix(ctx):
                    await cursor.execute(
                        '''
                        INSERT INTO prefixes
                        ( guild_id , prefix )
                        VALUES ( ? , ? )
                        ''' ,
                        (str(ctx.guild.id) , new_prefix , )
                    )
                    await database.commit()
                    return
                await cursor.execute(
                    '''
                    UPDATE prefixes
                    SET prefix = ? 
                    WHERE guild_id = ?
                    ''' ,
                    (new_prefix , str(ctx.guild.id) ,)
                )
                await database.commit()
                return
                
def setup(bot : Bot):
    bot.add_cog(Configurations(bot))