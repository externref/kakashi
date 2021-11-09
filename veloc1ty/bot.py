from disnake.ext.commands import Bot  , when_mentioned_or
from disnake import (
    Message , 
    Intents
)
from aiosqlite3 import connect 
from os import getenv , listdir

class Veloc1ty(Bot):
    async def get_prefix_for_guild(
        self ,bot : Bot ,  message : Message
    ):
        return await self.get_prefix_from_database(bot , message) 

    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix_for_guild ,
            case_insensitive = True ,
            intents = Intents.all()
        )
        for file in ['general']:
            try : 
                self.load_extension('cogs.'+file)
                print(file , 'loaded')
            except Exception as e:
                raise e

    async def on_ready(self):
        print(f'BOT IS READY\nNAME : {veloc1ty.user}\nID : {veloc1ty.user.id}')
        async with connect('database/prefixes.db') as database:
            async with database.cursor() as cursor:
                await cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS prefixes
                    ( guild_id TEXT , prefix TEXT)
                    '''
                )
                await database.commit()

    async def get_prefix_from_database(
        self , bot : Bot , message : Message
    ):
        async with connect('database/prefixes.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    '''
                    SELECT * FROM prefixes
                    WHERE guild_id = ?
                    ''' ,
                    (str(message.guild.id),)
                ) 
                prefix = data.fetchone()
                if not prefix :
                    return when_mentioned_or('+')(bot , message)
                return when_mentioned_or(prefix[1])(bot , message)
            
        
veloc1ty = Veloc1ty()
veloc1ty.run(getenv('TOKEN'))
