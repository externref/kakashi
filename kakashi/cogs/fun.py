from re import L
from disnake.ext.commands import (
    Cog ,
    Bot ,
    command ,
    bot_has_permissions ,
    cooldown ,
    BucketType
)
from disnake.ext.commands.context import Context
from aiohttp import ClientSession 
from disnake import Embed , User , File
from exts import EmbedColor
from asyncio import get_running_loop
from io import SEEK_CUR, BytesIO
from PIL import Image , ImageOps , ImageDraw

class FunCog(Cog , name='fun'):
    """
    Some fun commands 
    """
    def __init__(self , bot):
        self.bot = bot
        self.emoji = "🍿"
        self.banner = "https://cdn.discordapp.com/emojis/841163013969018913.png"
        self.help_desc = "Just some misc fun commands"
    
    @command(
        name = 'neko',
        description="Gets you a cute neko image"
    )
    @bot_has_permissions(embed_links=True , send_messages=True , read_message_history=True)
    @cooldown(2 , 10 , BucketType.user)
    async def neko_command(self , ctx : Context):
        """
        A random neko picture *Meow*
        """
        async with ClientSession() as session:
            res =await session.get("https://neko-love.xyz/api/v1/neko")
            data = await res.json()
        embed = Embed(color = await EmbedColor.color_for(ctx.guild)).set_author(name='Here\'s a neko for you',icon_url=self.bot.user.display_avatar)
        embed.set_image(url=data['url'])
        embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        await ctx.reply(
            embed=embed
        )

    @command(
        name='doggo',
        aliases=['dog'],
        description='Gets you a random doggo picture'
    )
    @bot_has_permissions(embed_links=True , send_messages=True , read_message_history=True)
    @cooldown(2 , 10 , BucketType.user)
    async def doggo_picture(self , ctx : Context):
        """
        A random doggo image
        """
        async with ClientSession() as session:
            res = await session.get("https://dog.ceo/api/breeds/image/random")
            data = await res.json()
        if data['status'] != 'success' : return await ctx.reply('Something went wrong while getting the image')
        await ctx.reply(
            embed = (Embed(
                title='Here\'s a doggo for you',
                color = await EmbedColor.color_for(ctx.guild)
            )
            .set_image(url=data['message'])
            .set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
            )
        )
       
    @command(
        name= 'cat',
        aliases=['meow'],
        description= 'Gets you a random cat image'
    )
    @bot_has_permissions(embed_links=True , send_messages=True , read_message_history=True)
    @cooldown(2 , 10 , BucketType.user)
    async def cat_picture(self , ctx : Context):
        """
        Get a random cat image
        """
        async with ClientSession() as session:
            res = await session.get('https://cataas.com/cat?json=true')
            try :
                data = await res.json()
                await ctx.reply(
                    embed = (Embed(
                        title='*Meow*',
                        color = await EmbedColor.color_for(ctx.guild)
                    )
                    .set_image(url="https://cataas.com"+data['url'])
                    .set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
                    )
                )
            except : await ctx.reply('Something went wrong while getting the image')

    @command(
        name = 'lyrics',
        description='Get lyrics for the song name you provide'
    )
    @bot_has_permissions(embed_links=True , send_messages=True , read_message_history=True)
    @cooldown(2 , 10 , BucketType.user)
    async def lyrics_command(self , ctx : Context ,*, song_name: str):
        """
        Search Song lyrics
        """
        async with ClientSession() as session:
            res = await session.get('https://some-random-api.ml/lyrics?title='+song_name)
            data = await res.json()
            try :
                embed = Embed(
                    title = data['title']+' by '+data['author'],
                    description=data['lyrics'][:750].replace('\n\n','\n')+f"[Keep reading....]({data['links']['genius']})",
                    color= await EmbedColor.color_for(ctx.guild)
                )
                embed.set_thumbnail(data['thumbnail']['genius'])
                embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
                await ctx.reply(
                    embed = embed
                )
            except: await ctx.reply("Something went wrong while getting those lyrics")
    
    @command(
       name='gay' ,
       aliases=['rainbow'],
       description='Applies a rainbow flag filter on the user\'s avatar'
    )
    @bot_has_permissions(embed_links=True , send_messages=True , read_message_history=True)
    @cooldown(2 , 10 , BucketType.user)
    async def cmd(self , ctx : Context , user : User = None):
        """
        Gay flag filter
        """
        user = user or ctx.author
        get_running_loop().run_in_executor(None ,await self.create_image_gay(user , ctx))
        embed = Embed(color=await EmbedColor.color_for(ctx.guild))
        embed.set_author(name=user.name,icon_url=user.display_avatar.url)
        embed.set_footer(text=f'Requested by {ctx.author}',icon_url=ctx.author.display_avatar)
        embed.set_image(url=f"attachment://gayimg{ctx.author.id}.png")
        await ctx.reply(
            embed = embed,
            file = File(f"trash/gayimg{ctx.author.id}.png")
        )
       
    
    async def create_image_gay(self , user : User , ctx : Context):
        avatar = Image.open(BytesIO(await user.display_avatar.read())).resize((216 , 216))
        filter = Image.open('images/gay_cover.png').resize((216 ,216))
        Image.blend(filter ,avatar , 0.4).save(f'trash/gayimg{ctx.author.id}.png')
        return 


def setup(bot : Bot):
    bot.add_cog(FunCog(bot))

