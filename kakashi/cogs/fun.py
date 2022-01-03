from disnake.ext.commands.cog import Cog
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.core import bot_has_permissions, cooldown
from disnake.ext.commands.core import command
from disnake.ext.commands.cooldowns import BucketType
from disnake.ext.commands.context import Context
from disnake.file import File
from disnake.embeds import Embed
from disnake.user import User
from aiohttp import ClientSession
from kakashi.core.exts import EmbedColor
from random import randint
from io import BytesIO
from PIL import Image


class FunCog(Cog, name="fun"):
    """
    Some fun commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🍿"
        self.banner = "https://cdn.discordapp.com/emojis/841163013969018913.png"
        self.help_desc = "Just some misc fun commands"

    @command(name="neko", description="Gets you a cute neko image")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def neko_command(self, ctx: Context):
        """
        A random neko picture *Meow*
        """
        async with ClientSession() as session:
            res = await session.get("https://neko-love.xyz/api/v1/neko")
            data = await res.json()
        embed = Embed(color=await EmbedColor.color_for(ctx.guild)).set_author(
            name="Here's a neko for you", icon_url=self.bot.user.display_avatar
        )
        embed.set_image(url=data["url"])
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.reply(embed=embed)

    @command(
        name="doggo", aliases=["dog"], description="Gets you a random doggo picture"
    )
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def doggo_picture(self, ctx: Context):
        """
        A random doggo image
        """
        async with ClientSession() as session:
            res = await session.get("https://dog.ceo/api/breeds/image/random")
            data = await res.json()
        if data["status"] != "success":
            return await ctx.reply("Something went wrong while getting the image")
        await ctx.reply(
            embed=(
                Embed(
                    title="Here's a doggo for you",
                    color=await EmbedColor.color_for(ctx.guild),
                )
                .set_image(url=data["message"])
                .set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.display_avatar,
                )
            )
        )

    @command(name="cat", aliases=["meow"], description="Gets you a random cat image")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def cat_picture(self, ctx: Context):
        """
        Get a random cat image
        """
        async with ClientSession() as session:
            res = await session.get("https://cataas.com/cat?json=true")
            try:
                data = await res.json()
                await ctx.reply(
                    embed=(
                        Embed(
                            title="*Meow*", color=await EmbedColor.color_for(ctx.guild)
                        )
                        .set_image(url="https://cataas.com" + data["url"])
                        .set_footer(
                            text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.display_avatar,
                        )
                    )
                )
            except:
                await ctx.reply("Something went wrong while getting the image")

    @command(name="hug", aliases=["cuddle"], description="Hugs your friend Owo")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def hug(self, ctx: Context, user: User = None):
        """
        Hug command
        """
        if not user:
            return await ctx.send(
                embed=Embed(
                    description=f"Ow , `{ctx.author.name}` needs a hug",
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
        async with ClientSession() as session:
            res = await session.get("https://some-random-api.ml/animu/hug")
            data: dict = await res.json()
            if not data.get("link"):
                return await ctx.reply(
                    "Something went wrong while getting the gif image", delete_after=10
                )
        embed = Embed(
            description=f"**{ctx.author.name}** hugs **{user.name}**",
            color=await EmbedColor.color_for(ctx.guild),
        ).set_image(url=data["link"])
        await ctx.reply(embed=embed)

    @command(name="wink", description="As the name suggests")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def wink_cmd(self, ctx: Context, user: User = None):
        """
        Wink command
        """
        async with ClientSession() as session:
            res = await session.get("https://some-random-api.ml/animu/wink")
            data: dict = await res.json()
            if not data.get("link"):
                return await ctx.reply(
                    "Something went wrong while getting the gif image", delete_after=10
                )
        description = f"**{ctx.author.name}** winks"
        if user:
            description += f"**{ctx.author.name}** winks at **{user.name}**"
        embed = Embed(
            description=description, color=await EmbedColor.color_for(ctx.guild)
        ).set_image(url=data["link"])
        await ctx.reply(embed=embed)

    @command(name="pat", aliases=["pet"], description="Send some cute pats :p")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def pat_cmd(self, ctx: Context, user: User = None):
        """
        Pat command
        """
        if not user:
            return await ctx.send(
                embed=Embed(
                    description=f"Could someone pat `{ctx.author.name}` ??",
                    color=await EmbedColor.color_for(ctx.guild),
                )
            )
        async with ClientSession() as session:
            res = await session.get("https://some-random-api.ml/animu/pat")
            data: dict = await res.json()
            if not data.get("link"):
                return await ctx.reply(
                    "Something went wrong while getting the gif image", delete_after=10
                )
        embed = Embed(
            description=f"**{ctx.author.name}** pats **{user.name}**",
            color=await EmbedColor.color_for(ctx.guild),
        ).set_image(url=data["link"])
        await ctx.reply(embed=embed)

    @command(name="lyrics", description="Get lyrics for the song name you provide")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def lyrics_command(self, ctx: Context, *, song_name: str):
        """
        Search Song lyrics
        """
        async with ClientSession() as session:
            res = await session.get(
                "https://some-random-api.ml/lyrics?title=" + song_name
            )
            data = await res.json()
            try:
                embed = Embed(
                    title=data["title"] + " by " + data["author"],
                    description=data["lyrics"][:750].replace("\n\n", "\n")
                    + f"[Keep reading....]({data['links']['genius']})",
                    color=await EmbedColor.color_for(ctx.guild),
                )
                embed.set_thumbnail(data["thumbnail"]["genius"])
                embed.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.display_avatar,
                )
                await ctx.reply(embed=embed)
            except:
                await ctx.reply("Something went wrong while getting those lyrics")

    @command(
        name="gay",
        aliases=["rainbow"],
        description="Applies a rainbow flag filter on the user's avatar",
    )
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    @cooldown(2, 10, BucketType.user)
    async def cmd(self, ctx: Context, user: User = None):
        """
        Gay flag filter
        """
        user = user or ctx.author
        await self.bot.loop.run_in_executor(
            None, await self.create_image_gay(user, ctx)
        )
        embed = Embed(color=await EmbedColor.color_for(ctx.guild))
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar
        )
        embed.set_image(url=f"attachment://gayimg{ctx.author.id}.png")
        await ctx.reply(embed=embed, file=File(f"trash/gayimg{ctx.author.id}.png"))

    async def create_image_gay(self, user: User, ctx: Context):
        avatar = (
            Image.open(BytesIO(await user.display_avatar.read()))
            .resize((512, 512))
            .convert("RGB")
        )
        filter = Image.open("images/gay_cover.png").resize((512, 512))
        Image.blend(avatar, filter, 0.3).save(f"trash/gayimg{ctx.author.id}.png")

    @command(name="ppsize", aliases=["pp"], description="A pp size generator")
    @bot_has_permissions(
        embed_links=True, send_messages=True, read_message_history=True
    )
    async def pp_size_cmd(self, ctx: Context, user: User = None):
        """
        Smol
        """
        user = user or ctx.author
        embed = Embed(
            description="3" + "=" * randint(0, 15) + "D",
            color=await EmbedColor.color_for(ctx.guild),
        ).set_author(name=f"{user.name}'s PP")
        await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(FunCog(bot))
