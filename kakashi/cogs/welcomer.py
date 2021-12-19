from disnake.ext.commands.core import guild_only
from disnake.ui.view import View
from . import (
    Cog ,
    Context , 
    Button,
    View,
    Bot    
)
from exts import EmbedColor
from aiosqlite import connect
from disnake import Color , Member , Embed , TextChannel 
from disnake.ext.commands import command , has_permissions ,bot_has_permissions
from typing import Union

class Welcomer(Cog , name='welcome'):
    """
    An awesome welcomer module
    """

    def __init__(self  , bot : Bot):
        self.bot : Bot = bot
        self.emoji = "👋"
        self.banner= "https://cdn.discordapp.com/emojis/840977619427262524.png"
        self.help_desc = "Greeting to the new users who joins your server"
        self.allowed_colors = {
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
        super().__init__()
    
    @Cog.listener()
    async def on_ready(self):
        await GuildDataBase.create_database()
    
    @command(
        name = 'welcome',
        hidden=True,
        description="Shows help for welcomer module"
    )
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def send_help_for_welcome(self , ctx : Context):
        """
        Shows this message
        """
        await ctx.send_help(self.bot.get_cog('welcome'))

    @command(
        name= 'welcome-message',
        aliases=['welcomemessage'],
        description = """
        Customise your Welcome Message ( Variables below allowed )
        ```bash\n
        $user : Name and tag of the User [ Sarthak_#0460 ]
        $usermention : Mention of the new Member [ <@!580034015759826944> ]
        $userid : Id of the Member [ 580034015759826944 ]
        $username : Username of the Member [ Sarthak_ ]
        $userdiscrim / $userdiscriminator : Discriminator of the User [ 0460 ]
        $server / $servername : Name of the Server [ VELOC1TY ]
        $membercount : Membercount of the Server [ 69 ] 
        $joined-discord : DD-MM-YYYY of account creatation [ 12 May 2019 ]
        $joined-server : DD-MM-YYYY of Server Join [ 23 Aug 2021 ]
        $joined-discord-timestamp : Timestamp Integer for Account Creation 
        $joined-server-timestamp : Timestamp Integer for Server Join\n
        ```
        """
        
    )
    @has_permissions(manage_guild=True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def welcome_message(self , ctx : Context, *, message : str):
        """
        Welcome message for the Server
        """
        if not await GuildDataBase.get_guild_data(ctx.guild.id):
            return await ctx.reply(
                embed = Embed(
                    description=f'{self.bot.my_emojis["cross"]} Setup a welcome channel first\nYou can use `{self.bot.get_prefix(ctx.message)}`'
                )
            )
        data = await GuildDataBase.get_guild_data(ctx.guild.id)
        await GuildDataBase.update_or_insert_guild_data(data[0], data[1] , message , data[3], data[4])
        await ctx.send(
            content='This is what the new message would look like',
            embed = Embed(
                description= await self.process_message(message , ctx.author),
                color = self.allowed_colors[str(data[3])],
                
            ).set_thumbnail(url =ctx.author.avatar.url or ctx.author.default_avatar.url).set_author(name = str(ctx.author), icon_url=(ctx.author.avatar or ctx.author.default_avatar).url)
        )


    @command(
        name = 'welcome-channel',
        aliases=['welcomechannel','set-welcome-channel','setwelcomechannel'],
        description = 'Setting up a welcome channel for the bot to send messages on new member joins\nThis can be set to `None` to avoid sending messages'
    )
    @has_permissions(manage_guild=True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def set_welcome_channel(self , ctx : Context , channel : Union[ TextChannel , str] ):
        """
        Setup Welcome Channel for the server
        """
        data = await GuildDataBase.get_guild_data(ctx.guild.id)
        if str(channel).lower() == 'none':
            if not await GuildDataBase.get_guild_data(ctx.guild.id):
                await ctx.reply(
                    embed = Embed(
                        description=f'{self.bot.my_emojis["cross"]} The server has no welcome channel setup yet so you cannot set it to None',
                        color=await EmbedColor.color_for(ctx.guild) 
                    )
                )
                return
            else:
                await GuildDataBase.update_or_insert_guild_data(ctx.guild.id , 'none' , data[2] , data[3], data[4])
                await ctx.reply(
                    embed = Embed(
                        description=f'{self.bot.my_emojis["tick"]} Welcome messages will no longer be sent',
                        color =  await EmbedColor.color_for(ctx.guild) 
                    )
                )
                return
        if channel not in ctx.guild.text_channels:
            return await ctx.reply(
                embed = Embed(
                    description=f'{self.bot.my_emojis["cross"]} The channel must be in the same server',
                    color = await EmbedColor.color_for(ctx.guild)
                )
            )
        if data :
            await GuildDataBase.update_or_insert_guild_data(ctx.guild.id , channel.id , data[2] , data[3], data[4])
        else :
            await GuildDataBase.update_or_insert_guild_data(ctx.guild.id , channel.id , "$usermention , welcome to $server" , 'cyan' , 'embedmessage' )
        await ctx.reply(
            embed = Embed(
                description= f'{ctx.bot.my_emojis["tick"]}  Set welcome channel to {channel.mention}' ,
                color =await EmbedColor.color_for(ctx.guild) 
            )
        )

    @command(
        name='welcome-color',
        aliases=['welcomecolor'],
        description='Set the color which appears in the welcoming embed for your server'
    )
    @has_permissions(manage_guild=True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def welcome_color(self , ctx : Context , color : str):
        """
        Custom Color for welcome messages
        """
        if not color in self.allowed_colors.keys():return await ctx.reply(embed=Embed(title='INVALID COLOR' , color = Color.red(),description=f'Available Colors : ```\n{",".join(c for c in self.allowed_colors.keys())}\n```'))

    @command(
        name = 'welcome-type',
        aliases= ['welcometype'],
        description = "Choose between embed messages and normal text messages ! `embed` and `text` are the available welcome types"
    )
    @has_permissions(manage_guild=True)
    @bot_has_permissions(embed_links = True , send_messages= True , read_message_history=True )
    async def change_welcome_type(self , ctx : Context , welcome_type : str):
        """
        Choose the welcome type for server
        """
        if not welcome_type in ['text','message'] : return await ctx.reply(embed=Embed(description=f"{self.bot.my_emojis['cross']} Type must be either `text` or `embed`",color= await EmbedColor.color_for(ctx.guild)))
        data = await GuildDataBase.get_guild_data(ctx.guild.id)
        if not data:
            return await ctx.reply(
                embed = Embed(
                    description=f'{self.bot.my_emojis["cross"]} The server has no welcome channel setup yet .',
                    color=await EmbedColor.color_for(ctx.guild) 
                )
            )
        await GuildDataBase.update_or_insert_guild_data(data[0],data[1],data[2],data[3],f"{welcome_type}message")
        await ctx.reply(
            embed = Embed(
                description=f"{self.bot.my_emojis['tick']} Changed welcome type to `{welcome_type}`",
                color = await EmbedColor.color_for(ctx.guild)
            )
        )
            
        

    @Cog.listener()
    async def on_member_join(self , member: Member):
        data = await GuildDataBase.get_guild_data(member.guild.id)
        if not data : return
        message = data[2]
        if data[1] == 'none' : return
        channel = self.bot.get_channel(int(data[1]))
        if not channel : return
        welcome_message =await self.process_message(message , member)
        if data[4] == 'textmessage':
            content =  welcome_message 
            try : await channel.send(content = content)
            except : pass
        elif data[4] == 'embedmessage':
            embed = Embed(
            description= welcome_message , 
            color = self.allowed_colors[data[3]]   
            ).set_author(name = str(member), icon_url=(member.avatar or member.default_avatar).url)
            embed.set_thumbnail(url=(member.avatar or member.default_avatar).url)
            embed.set_footer()
            try : await channel.send(embed = embed)
            except : pass

    async def process_message(self , message , member):
        message_to_return=  (message
                                .replace('$usermention' , str(member.mention))
                                .replace('$userid' , str(member.id))
                                .replace('$username' , str(member.name))
                                .replace('$userdiscriminator' , str(member.discriminator))
                                .replace('$userdiscrim' , str(member.discriminator))
                                .replace('$user' , str(member))
                                .replace('$servername' , str(member.guild.name))
                                .replace('$server', str(member.guild.name))
                                .replace('$membercount' , str(member.guild.member_count))
                                .replace('$joined-discord-timestamp' , str(int(member.created_at.timestamp())))
                                .replace('$joined-server-timestamp' , str(int(member.joined_at.timestamp())))
                                .replace('$joined-discord' , str(member.created_at.strftime('%d %b %y')))
                                .replace('$joined-server' , str(member.joined_at.strftime('%d %b %y')))
                             )
        return message_to_return
        


class GuildDataBase:
    async def create_database():
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                await cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS welcomer 
                    ( guild_id TEXT , channel_id TEXT , message TEXT , color TEXT , welcome_type TEXT)
                    """
                )
            await database.commit()

    async def get_guild_data(guild_id : str):
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    """
                    SELECT * FROM welcomer 
                    WHERE guild_id = ?
                    """ ,
                    (str(guild_id) ,)
                )
                guild_data = await data.fetchone()
                if not guild_data : return 
                return guild_data
    
    async def update_or_insert_guild_data(guild_id :str , channel_id :str, message : str  , color : str = 'blue' , type : str = 'embedmessage' ) -> None:
        async with connect('database/guild.db') as database:
            async with database.cursor() as cursor:
                data = await cursor.execute(
                    """
                    SELECT * FROM welcomer 
                    WHERE guild_id = ?
                    """ ,
                    (str(guild_id), )
                )
                is_data = await data.fetchone()
                if is_data:
                    await cursor.execute(
                        """
                        UPDATE welcomer
                        SET channel_id = ? , message = ? , color = ? , welcome_type = ?
                        where guild_id = ?
                        """ , 
                        (str(channel_id), str(message) , str(color) , str(type) , str(guild_id),)
                    )
                    await database.commit()
                else:
                    await cursor.execute(
                        """
                        INSERT INTO welcomer
                        ( guild_id , channel_id , message , color , welcome_type )
                        VALUES ( ? , ? , ? , ? , ?)
                        """ ,
                        (str(guild_id) , str(channel_id) , message , color , type , )
                    )   
                    await database.commit()
                return



def setup(bot : Bot):
    bot.add_cog(Welcomer(bot))


