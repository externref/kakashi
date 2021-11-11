from . import (
    Cog ,
    Button ,
    Bot ,
    Context , 
    View , 
)
from discord.ext.commands import command

class Configurations(Cog):
    def __init__(self , bot : Bot):
        self.bot = bot

    @command()


def setup(bot : Bot):
    bot.add_cog(Configurations(bot))