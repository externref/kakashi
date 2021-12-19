from disnake.ext.commands.core import has_permissions
from disnake.interactions.application_command import ApplicationCommandInteraction
from . import (
    Cog ,
    Button ,
    Bot ,
    Context , 
    View , 
)
from exts import EmbedColor
from disnake.ext.commands import command , has_guild_permissions , bot_has_permissions , has_permissions ,slash_command
from aiosqlite import connect
from disnake import Embed ,Color, Option,OptionType

list_colors = ['red', 'blue', 'yellow', 'purple', 'darkblue', 'white', 'black', 'pink', 'cyan', 'skyblue', 'green']
class Configurations(Cog , name='config'):
    """
    Bot Configurations for your server
    """
    def __init__(self , bot : Bot):
        self.emoji = "⚙️"
        self.bot = bot
        self.help_desc = "Commands that make the bot highly customisable for the server ;)\n"
        self.banner = "https://cdn.discordapp.com/emojis/921039329416052777.png"
        self.colors = {
            'red' : Color.red(),
            'blue' : Color.blue(),
            'yellow' : Color.yellow(),
            'purple' : Color.purple(),
            'darkblue' : Color.dark_blue(),
            'white' : 0xFFFFFF,
            'black' : 0x000000,
            'pink' : 0xFFC0CB ,
            'cyan' : 0x00FFFF ,
            'skyblue' : 0x87CEEB ,
            'green' : Color.green()
        }

    @command(
        name='bot-color',
        aliases=['botcolor','embedcolors'],
        description= f'Choose a custom Embed color for embeds send in your server , You can choose from :\n`{"` ,`".join(list_colors)}`'
    )
    @has_permissions(manage_guild =True)
    async def change_embed_message_colors(self , ctx : Context , color):
        """
        Change bot's Embeds color
        """
        if not color.lower() in self.colors.keys(): return await ctx.reply(embed=Embed(title='INVALID COLOR' , color = Color.red(),description=f'Available Colors : ```\n{",".join(c for c in self.colors.keys())}\n```'))
        await DataBaseHandler.add_color(ctx , color)        
        await ctx.reply(
            embed= Embed(
                description=f'Changed bot\'s appearance color to {color}',
                color = Color.green()
            )
        )


    @command(
        name = 'prefix' ,
        description ='Check the bot\'s prefix for the guild just in case you\'re lost'
    )
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True)
        
    async def send_prefix(self , ctx : Context):
        """
        Send Bot's prefix for the server 
        """
        await ctx.reply(
            embed = Embed(
                color = await EmbedColor.color_for(ctx.guild) ,
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
        """
        Change Bot\'s prefix for a server
        """
        if any([letter for letter in new_prefix if letter in ['@' , '`' , '#']]):
            return await ctx.reply(
                embed = Embed(
                    description=f"{ctx.bot.my_emojis['cross']} Bot prefix Cannot contain \` , `@` or `#` characters due to discord markdown .",
                    color = await EmbedColor.color_for(ctx.guild)
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
        aliases = ['prefix-clear'],
        description='Change bot\'s prefix back to `.`'
    )
    @has_guild_permissions(manage_guild=True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def remove_prefix_for_guild(self , ctx : Context):
        """
        Reset Server Prefix
        """
        old_prefix = self.bot.get_prefix(ctx.message)
        await DataBaseHandler.insert_or_update_prefix(ctx , '.')
        await ctx.reply(
            embed = Embed(
                description=f'{self.bot.my_emojis["tick"]} Changed prefix back from `{old_prefix}` to `.`'
            )
        )

def setup(bot : Bot):
    bot.add_cog(Configurations(bot))
    
class DataBaseHandler:
    async def add_color(ctx : Context , color):
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                data=await cursor.execute(
                    """
                    SELECT * FROM colors
                    WHERE guild_id = ?
                    """,
                    (str(ctx.guild.id),)
                )
                d = await data.fetchone()
                if not d:
                    await cursor.execute(
                        """
                        INSERT INTO colors
                        ( guild_id , color )
                        VALUES (? , ?)
                        """,
                        (str(ctx.guild.id) , color.lower() ,)
                    )
                    await database.commit()
                else:
                    await cursor.execute(
                        """
                        UPDATE colors
                        SET color = ?
                        WHERE guild_id = ?
                        """,
                        (color.lower(), str(ctx.guild.id),)
                    )
                    print('added')
                    await database.commit()

    async def get_prefix(ctx : Context):
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """ ,
                    (str(ctx.guild.id),)
                ) 
                prefix = await data.fetchone()
                if not prefix :
                    return None 
                return prefix[1]

    async def insert_or_update_prefix(ctx : Context , new_prefix : str):
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                if not await DataBaseHandler.get_prefix(ctx):
                    await cursor.execute(
                        """
                        INSERT INTO prefixes
                        ( guild_id , prefix )
                        VALUES ( ? , ? )
                        """ ,
                        (str(ctx.guild.id) , new_prefix , )
                    )
                    await database.commit()
                    return
                await cursor.execute(
                    """
                    UPDATE prefixes
                    SET prefix = ? 
                    WHERE guild_id = ?
                    """ ,
                    (new_prefix , str(ctx.guild.id) ,)
                )
                await database.commit()
                return
                
