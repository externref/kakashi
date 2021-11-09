from . import (
    Cog ,
    Bot ,
    Context
)
from datetime import datetime
from disnake.ext.commands import command
from disnake import Color , Embed

class General_CMDS(Cog):
    '''
    Basic Bot Commands 
    '''
    
    @command(
        name = 'ping',
        aliases = ['latency']
    )
    async def ping_command( self , ctx : Context ):
        e = datetime.now()
        msg = await ctx.reply(
            embed = Embed(
                color = Color.blue()
            ).add_field(name='Bot Latency',value='```yaml\nCalc ms\n```').add_field(name='Script Latency',value='```yaml\nCalc ms\n```')
        )
        await msg.edit(
            embed = Embed(
                color = Color.blue()
            ).add_field(name='Bot Latency',value=f'```yaml\n{round(ctx.bot.latency*1000)}ms\n```').add_field(name='Script Latency',value=f'```yaml\n{round((e-datetime.now()).microseconds/1000)}ms\n```')
        )
    
def setup(bot : Bot):
    bot.add_cog(General_CMDS(bot))