import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import pymysql, json


transfer = {
    "0" : "None",
    "1" : "Choice",
    "2" : "Complete"
}



class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open('dbconfig.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]



    @nextcord.slash_command(name="config", description="Edit your guild settings config")
    async def config(self,
        ctx: Interaction
        ):
        pass

    @config.subcommand(name="enable", description="Enable options for your guild settings config")
    async def config_enable(self,
        ctx: Interaction,
        verifyrole : nextcord.Role = SlashOption(
            name="verifyrole",
            description="The role given when users successfully verify.",
            required=False
        ),
        unverifiedrole : nextcord.Role = SlashOption(
            name="unverifiedrole",
            description="The role given to users when they join the server.",
            required=False
        ),
        logchannel : GuildChannel = SlashOption(
            name="logchannel",
            description="Channel to send verification logs to",
            required=False,
            channel_types=[nextcord.ChannelType.text]
        ),
        captchatype : str = SlashOption(
            name="captchatype",
            description="Choose the type of captcha to be sent (Use `/captchatype info` to see the different options)",
            required=False,
            choices={"None" : "0", "Complete" : "2"}
        ),
        autokick : int = SlashOption(
            name="autokick",
            description="Select the minimum age for an account to stay in the server (**In days**)",
            required=False
        ),
        autocaptcha : str = SlashOption(
            name="autocaptcha",
            description="Enable auto captcha which will automatically start verification on new users who join the server",
            required=False,
            choices={"Enabled" : "enabled"}
        )
        ):
        global transfer
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{ctx.guild.id}'")
        data = cur.fetchall()
        if not data:
            cur.execute(f"INSERT INTO guild_configs (id) VALUES ('{ctx.guild.id}')")
            conn.commit()
            conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
            cur = conn.cursor()
        if not verifyrole and not unverifiedrole and not logchannel and not captchatype and not autokick and not autocaptcha:
            embed=nextcord.Embed(title=f"Error", description=f"It seems you didn't select any options. Make sure you select any you want to change and try again", colour=0xadd8e6)
            await ctx.send(embed=embed)
            return
        embed=nextcord.Embed(title=f"Guild Config Updated", description=f"You have successfully updated your guild config. A list of changes is listed below:", colour=0xadd8e6)
        if verifyrole:
            cur.execute(f"UPDATE guild_configs SET verifyrole='{verifyrole.id}' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Verify role", value=f"{verifyrole.mention} ({verifyrole.id})")
        if unverifiedrole:
            cur.execute(f"UPDATE guild_configs SET unverifiedrole='{unverifiedrole.id}' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Unverified role", value=f"{unverifiedrole.mention} ({unverifiedrole.id})")
        if logchannel:
            cur.execute(f"UPDATE guild_configs SET logchannel='{logchannel.id}' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Log channel", value=f"{logchannel.mention} ({logchannel.id})")
        if captchatype:
            cur.execute(f"UPDATE guild_configs SET captchatype='{captchatype}' WHERE id='{ctx.guild.id}'")
            captchaname = transfer[captchatype]
            embed.add_field(name="Captcha type", value=f"{captchaname}")
        if autokick:
            if not autokick > 0:
                embed.add_field(name="Auto kick", description=f"Cannot set auto kick to less than 1 day")
                return
            cur.execute(f"UPDATE guild_configs SET autokick='{autokick}' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Auto kick", value=f"{autokick} days")
        if autocaptcha:
            cur.execute(f"UPDATE guild_configs SET autoveri='{autocaptcha}' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Auto captcha", value=f"Auto captcha has been enabled")
        conn.commit()
        await ctx.send(embed=embed)
        

    @config.subcommand(name="disable", description="Disable options for your guild settings config")
    async def config_disable(self,
        ctx: Interaction,
        verifyrole : str = SlashOption(
            name="verifyrole",
            description="The role given when users successfully verify.",
            required=False,
            choices={"Disable" : "disable"}
        ),
        unverifiedrole : str = SlashOption(
            name="unverifiedrole",
            description="The role given to users when they join the server.",
            required=False,
            choices={"Disable" : "disable"}
        ),
        logchannel : str = SlashOption(
            name="logchannel",
            description="Channel to send verification logs to",
            required=False,
            choices={"Disable" : "disable"}
        ),
        autokick : str = SlashOption(
            name="autokick",
            description="Select the minimum age for an account to stay in the server (**In days**)",
            required=False,
            choices={"Disable" : "disable"}
        ),
        autocaptcha : str = SlashOption(
            name="autocaptcha",
            description="Enable auto captcha which will automatically start verification on new users who join the server",
            required=False,
            choices={"Disable" : "disable"}
        )
        ):
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{ctx.guild.id}'")
        data = cur.fetchall()
        if not data:
            cur.execute(f"INSERT INTO guild_configs (id) VALUES ('{ctx.guild.id}')")
            conn.commit()
            conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
            cur = conn.cursor()
        if not verifyrole and not unverifiedrole and not logchannel and not autokick and not autocaptcha:
            embed=nextcord.Embed(title=f"Error", description=f"It seems you didn't select any options. Make sure you select any you want to change and try again", colour=0xadd8e6)
            await ctx.send(embed=embed)
            return
        embed=nextcord.Embed(title=f"Guild Config Updated", description=f"You have successfully updated your guild config. A list of changes is listed below:", colour=0xadd8e6)
        if verifyrole:
            cur.execute(f"UPDATE guild_configs SET verifyrole=NULL WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Verify role", value=f"None")
        if unverifiedrole:
            cur.execute(f"UPDATE guild_configs SET unverifiedrole=NULL WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Unverified role", value=f"None")
        if logchannel:
            cur.execute(f"UPDATE guild_configs SET logchannel=NULL WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Log channel", value=f"None")
        if autokick:
            cur.execute(f"UPDATE guild_configs SET autokick='0' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Auto kick", value=f"Off")
        if autocaptcha:
            cur.execute(f"UPDATE guild_configs SET autoveri='no' WHERE id='{ctx.guild.id}'")
            embed.add_field(name="Auto captcha", value=f"Off")
        conn.commit()
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Settings(client))