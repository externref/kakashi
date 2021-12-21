from disnake.ext.commands import (
    Context , 
    Cog , 
    Bot ,
    command ,
    is_owner ,
    MemberNotFound ,
    UserNotFound , 
    RoleNotFound ,
    MissingPermissions ,
    BotMissingPermissions ,
    NotOwner ,
    CommandOnCooldown,
    CommandError,
    BadUnionArgument
)
from disnake import Embed
from exts import EmbedColor

class Developer(Cog , name='botbase'):
    def __init__(self , bot : Bot):
        self.bot = bot
    
    @command(
        name = 'refresh',
        aliases=['reboot']
    )
    @is_owner()
    async def owner_reload_cogs(self , ctx : Context):
        for cog in self.bot.cog_list[1:] :
            try : 
                self.bot.reload_extension('cogs.'+cog)
                print(cog , 'loaded')
            except Exception as e:
                raise e
        await ctx.reply("Reloaded `" + "` , `".join(cog+'.py' for cog in self.bot.cog_list) +'` files')

    @Cog.listener('on_command_error')
    async def error_handler(self , ctx : Context , error : CommandError ):
        if isinstance( error , NotOwner ):
            description , emoji = f"`{ctx.command.name}` is an owner only command" , self.bot.my_emojis['cross']
        elif isinstance( error , MissingPermissions):
            description , emoji = f"You need `{'` , `'.join(error.missing_permissions).replace('guild','server')}` permission(s) to run this command" , self.bot.my_emojis['cross']
        elif isinstance( error , BotMissingPermissions):
            return await ctx.send("Bot requires `{'` , `'.join(error.missing_permissions).replace('guild','server')}` permission(s) to run this command")
        elif isinstance( error , RoleNotFound ):
            description , emoji = f"Role `{error.argument}` was not found" , self.bot.get_emoji(888098945883050065)
        elif isinstance( error , MemberNotFound) :
            description , emoji = f"Member `{error.argument}` was not found" , self.bot.get_emoji(888098801326383104)
        elif isinstance( error , UserNotFound) :
            description , emoji = f"User `{error.argument}` was not found" ,  self.bot.get_emoji(888098801326383104)
        elif isinstance( error , BadUnionArgument ):
            description , emoji = f"Invalid {error.param.name} supplied"  , self.bot.my_emojis['cross']
        elif isinstance( error , CommandOnCooldown ):
            description , emoji = f"You need to wait for {int(error.retry_after)} seconds before trying again" , self.bot.get_emoji(841711427052240927)
        else :  raise error
        embed = Embed(
            description= str(emoji)+ " " + description ,
            color = await EmbedColor.color_for(ctx.guild)
        )
        await ctx.reply(
            embed = embed ,
            delete_after = 10
        )

def setup(bot : Bot):
    bot.add_cog(Developer(bot))

