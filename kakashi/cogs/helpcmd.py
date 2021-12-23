from disnake.ext.commands import HelpCommand ,  Context , Cog , Bot , Command , bot_has_permissions
from disnake import Embed , SelectOption , MessageInteraction , Message ,ButtonStyle
from exts import EmbedColor
from asyncio import sleep
from datetime import datetime
from typing import Union
from disnake.ui import View , Select , Button


class MyHelp(HelpCommand):
    
    async def send_bot_help(self, mapping):
        categories = self.context.bot.cogs
        embed = Embed(
            color = await EmbedColor.color_for(self.context.guild),
            timestamp=datetime.now()
        )
        for cog in categories:
            cog : Cog = self.context.bot.get_cog(cog)
            if cog.qualified_name in ['HelpCog','Jishaku' , 'botbase']: continue
            embed.add_field(
                name = f"{cog.emoji} {cog.qualified_name.upper()} COMMANDS",
                value = f"`{(await self.context.bot.get_prefix(self.context.message))[2]}help {cog.qualified_name}` ; [{len(cog.get_commands())} commands] {cog.__doc__.replace('    ','')}",
                inline=False
            )
        embed.set_author(name=f'{self.context.bot.user.name.upper()} HELP',icon_url=self.context.bot.user.display_avatar)
        embed.set_thumbnail(url=self.context.bot.user.display_avatar)
        embed.set_footer(text=f'Requested by {self.context.author}',icon_url=self.context.author.display_avatar)
        view = HelpView()
        view.add_item(HelpDropMenu(self.context))
        view.add_item(InviteButton(self.context))
        #view.add_item(VoteButton(self.context))
        view.message = await self.context.reply(
            embed=embed,
            view = view
        )
    
    async def send_cog_help(self , cog : Cog):
        await self.context.reply(
            embed = await embed_for_cog( self ,cog , self.context)
        )
    
    async def send_command_help(self, command : Command):
        
        help_dict={
            'Name' : command.name ,
            'Aliases' : " , ".join(command.aliases) or "No aliases",
            'Description' : command.description ,
            'Usage' : "```\n"+(await self.context.bot.get_prefix(self.context.message))[2]+command.name +" "+ command.signature+"```"
        }
        desc = "\n".join("**"+key+" :** "+help_dict[key] for key in help_dict)
        embed = Embed(
            description = desc,
            color = await EmbedColor.color_for(self.context.guild)
        )
        embed.set_author(name=f"{command.name.upper()} COMMAND",icon_url=self.context.bot.user.display_avatar)
        embed.set_footer(text=f'Requested by {self.context.author}',icon_url=self.context.author.display_avatar)
        await self.context.reply(
            embed=embed
        )
  


class HelpView(View):
    message : Message
    def __init__(self ):
        super().__init__(
            timeout=60
        )
    async def on_timeout(self):
        self.children[0].disabled = True
        self.remove_item(self.children[1])
        await self.message.edit(
            content= '`Menu Options` is no longer active',
            view=self
        )

class InviteButton(Button):
    def __init__(self , ctx : Context):
        super().__init__(
            emoji= "🔗",
            label = 'Invite',
            url = ctx.bot.invite_url,
            style = ButtonStyle.url
        )

class VoteButton(Button):
    def __init__(self , ctx : Context):
        super().__init__(
            emoji= ctx.bot.get_emoji(841178289171333120),
            label = 'Vote',
            disabled=True,
            url = f"https://top.gg/bot"+str(ctx.bot.user.id),
            style = ButtonStyle.url
        )

class ServerButton(Button):
    def __init__(self , ctx : Context):
        super().__init__(
            emoji= ctx.bot.get_emoji(840977048734269451),
            label = 'Invite',
            url = ctx.bot.invite_url,
            style = ButtonStyle.url
        )
        
class HelpDropMenu(Select):
    def __init__(self , ctx : Context):
        self.context = None
        self.bot = ctx.bot
        self.context = ctx
        opts = []
        for cog in ctx.bot.cogs:
            cog = ctx.bot.get_cog(cog)
            if cog.qualified_name in ['HelpCog','Jishaku' , 'botbase']: continue
            opts.append(
                SelectOption(label=f"{cog.qualified_name.upper()} COMMANDS",emoji=cog.emoji,description=cog.__doc__,value=cog.qualified_name )
            )
        super().__init__(
            placeholder='Choose Category',
            options=opts,
        )
    async def callback(self, interaction: MessageInteraction):
        cog = [self.bot.get_cog(cog) for cog in self.bot.cogs if interaction.values[0]==self.bot.get_cog(cog).qualified_name]
        await interaction.message.edit(
            embed = await embed_for_cog(self , cog[0] , interaction)
        )
        await interaction.response.send_message(f'Showing help for {cog[0].qualified_name.upper()} COMMANDS',ephemeral=True)
        

class HelpCog(Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelp()
        bot.help_command.cog = self
        
def setup(bot : Bot):
    bot.add_cog(HelpCog(bot))

async def embed_for_cog(self , cog : Cog , inter : Union[Context , MessageInteraction]):
    commands = cog.get_commands()
    desc : str = cog.help_desc + "\nUse `help <command-name>` for more info\n\n"
    for command in commands:
        desc=desc +"`" +(await self.context.bot.get_prefix(self.context.message))[2]+ command.name + "` : "+ command.short_doc+"\n"
    embed = Embed(
        color = await EmbedColor.color_for(inter.guild),
        description=desc
    ).set_author(name=f"{cog.qualified_name.upper()} COMMANDS",icon_url=inter.guild.me.display_avatar)
    embed.set_footer(text=f"Requested by : {inter.author}",icon_url=inter.author.display_avatar)
    embed.set_thumbnail(url=cog.banner) 
    return embed

    