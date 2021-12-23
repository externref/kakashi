from disnake.ext.commands import Bot , when_mentioned_or  
from disnake import (
    Message , 
    Intents ,
    AllowedMentions
)
from aiosqlite import connect 
from os import getenv 
from time import time

class Kakashi(Bot):
    
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix_for_guild ,
            case_insensitive = True ,
            intents = Intents.all() ,
            strip_after_prefix = True ,
            test_guilds = [int(getenv('MY_GUILD'))],
            allowed_mentions = AllowedMentions(
                everyone=False ,
                replied_user=False ,
                roles=False
            ),
            description = "A multipurpose customizable bot with server management , utility and fun commands"
        )
        self.boot_time = time()
        self.ran_commands = 0
        self.server_invite = 'PgmzbNbf37'
        self.banner = 'https://i.imgur.com/kFiFzrC.jpg'
        self.load_extension('jishaku')
        self.cog_list = ['dev','info','fun', 'configs','welcomer','utilities','general','helpcmd']
        for file in self.cog_list :
            try : 
                self.load_extension('cogs.'+file)
                print(file , 'loaded')
            except Exception as e:
                raise e
    
    async def get_prefix_for_guild(
        self ,bot : Bot ,  message : Message
    ):
        return await self.get_prefix_from_database(bot , message) 

    
    async def add_emojis(self):
        self.my_emojis = {
            'wave' : self.get_emoji(898560210292068412) ,
            'wave2' : self.get_emoji(892593887833653258) ,
            'tick_static' : self.get_emoji(888120845749334016),
            'cross_static' : self.get_emoji(888120623824515131),
            'tick' : self.get_emoji(909105537587765279),
            'cross' : self.get_emoji(909105779578126347)
        }

    
    async def on_ready(self):
        print(f'BOT IS READY\nNAME : {self.user}\nID : {self.user.id}')
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS prefixes
                    ( guild_id TEXT , prefix TEXT)
                    """
                )
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS colors
                    ( guild_id TEXT , color TEXT )
                    """
                )
                await database.commit()
        await self.add_emojis()
        self.bot_owner = self.get_user(580034015759826944)
        self.invite_url = f'https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=3691367512&scope=bot%20applications.commands'
            
        
    async def get_prefix_from_database(
        self , bot : Bot , message : Message
    ):
        if not message.guild : return '.'
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    """
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    """ ,
                    
                    (str(message.guild.id),)
                ) 
                prefix = await data.fetchone()
                if not prefix :
                    return when_mentioned_or('.')(bot , message)
                return when_mentioned_or(prefix[1])(bot , message)

if __name__ == '__main__':            
    Kakashi = Kakashi()

