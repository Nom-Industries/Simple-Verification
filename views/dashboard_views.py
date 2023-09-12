import nextcord, pymysql, asyncio
from nextcord.interactions import Interaction
from utils import DBENDPOINT, DBNAME, DBPASS, DBUSER, COLOUR_MAIN, create_error_embed, DISCORDLINK, create_success_embed, PREMIUMLINK, generate_dashboard
from nextcord import Interaction
from .role_select import RoleSelect, ChannelSelect
from .length_modal import LengthModal


class AutoVerificationButton(nextcord.ui.Button):
    def __init__(self, msg, premium: bool = False):
        if premium:
            super().__init__(label="Toggle Auto Verification", style=nextcord.ButtonStyle.blurple, disabled=False)
        else:
            super().__init__(label="Toggle Auto Verification", style=nextcord.ButtonStyle.blurple, disabled=True)
        self.msg = msg

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await interaction.send(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            conn.commit()
            self.stop()
            return
        
        if data[0][6] == "no":
            cur.execute(f"UPDATE `guild_configs` SET autoveri = 'enabled' WHERE id='{interaction.guild.id}'")
            embed = create_success_embed(title="Success", description="Successfully enabled autoverification.")
        else:
            cur.execute(f"UPDATE `guild_configs` SET autoveri = 'no' WHERE id='{interaction.guild.id}'")
            embed = create_success_embed(title="Success", description="Successfully disabled autoverification.")

        conn.commit()
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()
        eembed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=eembed)
        await interaction.send(embed=create_success_embed(title="Success", description="Successfully updated your auto verification setting."), ephemeral=True)

class AutoVerificationButton(nextcord.ui.Button):
    def __init__(self, msg, premium: bool = False):
        if premium:
            super().__init__(label="Set Min Captcha Length", style=nextcord.ButtonStyle.blurple, disabled=False)
        else:
            super().__init__(label="Set Min Captcha Length", style=nextcord.ButtonStyle.blurple, disabled=True)
        self.msg = msg

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await interaction.send(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            conn.commit()
            self.stop()
            return
        
        if data[0][6] == "no":
            cur.execute(f"UPDATE `guild_configs` SET autoveri = 'enabled' WHERE id='{interaction.guild.id}'")
            embed = create_success_embed(title="Success", description="Successfully enabled autoverification.")
        else:
            cur.execute(f"UPDATE `guild_configs` SET autoveri = 'no' WHERE id='{interaction.guild.id}'")
            embed = create_success_embed(title="Success", description="Successfully disabled autoverification.")

        conn.commit()
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()
        eembed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=eembed)
        await interaction.send(embed=create_success_embed(title="Success", description="Successfully updated your auto verification setting."), ephemeral=True)
            

class DashboardButtons(nextcord.ui.View):
    def __init__(self, msg, premium: bool = False):
        super().__init__(timeout=300)
        self.premium = premium
        self.msg = msg
        self.add_item(AutoVerificationButton(msg = msg, premium=premium))

    @nextcord.ui.button(label="Set Verification Roles", style=nextcord.ButtonStyle.blurple, disabled=False)
    async def set_verification_role(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if self.premium:
            rselect = RoleSelect(minvalue=1, maxvalue=10, text="Select Verification Roles")
            embed = nextcord.Embed(title="Select Verification Roles", description=f"Select the role you want members to recieve when they verify. \nAs a [premium]({PREMIUMLINK}) user you can select up to `10` roles!", color=COLOUR_MAIN)
        else:
            rselect = RoleSelect(minvalue=1, maxvalue=1, text="Select Verification Roles")
            embed = nextcord.Embed(title="Select Verification Roles", description=f"Select the role you want members to recieve when they verify. \nAs a standard user you can select `1` role. \nUpgrade to [premium]({PREMIUMLINK}) to be able to select up to `10` roles!", color=COLOUR_MAIN)
        
        msg = await interaction.send(embed=embed, view=rselect, ephemeral=True)
        await rselect.wait()
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await msg.edit(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            conn.commit()
            self.stop()
            return
        
        if rselect.values:
            ids = ",".join([str(role.id) for role in rselect.values])
        else:
            ids = None

        cur.execute(f"UPDATE `guild_configs` SET verifyrole = '{ids}' WHERE id='{interaction.guild.id}'")
        conn.commit()

        await asyncio.sleep(0.3)

        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()

        embed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=embed)
        await msg.edit(embed=create_success_embed(title="Success", description="Successfully updated verification roles."), view=None)

    @nextcord.ui.button(label="Set Unverified Roles", style=nextcord.ButtonStyle.blurple, disabled=False)
    async def set_unverified_role(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if self.premium:
            rselect = RoleSelect(minvalue=1, maxvalue=10, text="Select Unverified Roles")
            embed = nextcord.Embed(title="Select Unverified Roles", description=f"Select the roles you want members to have while they are unverified. \nAs a [premium]({PREMIUMLINK}) user you can select up to `10` roles!", color=COLOUR_MAIN)
        else:
            rselect = RoleSelect(minvalue=1, maxvalue=1, text="Select Unverified Roles")
            embed = nextcord.Embed(title="Select Unverified Roles", description=f"Select the roles you want members to have while they are unverified. \nAs a standard user you can select `1` role. \nUpgrade to [premium]({PREMIUMLINK}) to be able to select up to `10` roles!", color=COLOUR_MAIN)
        
        msg = await interaction.send(embed=embed, view=rselect, ephemeral=True)
        await rselect.wait()
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await msg.edit(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            conn.commit()
            self.stop()
            return
        
        if rselect.values:
            ids = ",".join([str(role.id) for role in rselect.values])
        else:
            ids = None

        cur.execute(f"UPDATE `guild_configs` SET unverifiedrole = '{ids}' WHERE id='{interaction.guild.id}'")
        conn.commit()

        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()

        embed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=embed)
        await msg.edit(embed=create_success_embed(title="Success", description="Successfully updated unverified roles."), view=None)


    @nextcord.ui.button(label="Set Log Channel", style=nextcord.ButtonStyle.blurple, disabled=False)
    async def set_log_channel(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        embed = nextcord.Embed(title="Select Log Channel", description="Select the channel you want logs to be sent in. \nYou can select `1` channel.", color=COLOUR_MAIN)
        cselect = ChannelSelect(minvalue=1, maxvalue=1, text="Select a Channel")
        msg = await interaction.send(embed=embed, view=cselect)
        await cselect.wait()
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await msg.edit(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            conn.commit()
            self.stop()
            return

        if cselect.values:
            id = cselect.values[0]
        else:
            id = None

        cur.execute(f"UPDATE `guild_configs` SET logchannel = '{id.id}' WHERE id='{interaction.guild.id}'")
        conn.commit()
        
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()

        embed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=embed)
        await msg.edit(embed=create_success_embed(title="Success", description="Successfully updated log channel."), view=None)

    @nextcord.ui.button(label="Set Autokick Account Age", style=nextcord.ButtonStyle.blurple, disabled=False)
    async def set_autokick_account_age(self, button: nextcord.ui.Button, interaction: Interaction):
        form = LengthModal()
        await interaction.response.send_modal(modal=form)
        await form.wait()

        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await interaction.send(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None, ephemeral=True)
            conn.commit()
            self.stop()
            return
        
        try:
            length = int(form.age)
        except:
            await interaction.send(embed=create_error_embed(title="Error", description="An invalid duration was supplied, the duration must be a whole positive number"), ephemeral=True)
            return

        if length < 0:
            await interaction.send(embed=create_error_embed(title="Error", description="An invalid duration was supplied, the duration must be a whole positive number"), ephemeral=True)
            return
        
        cur.execute(f"UPDATE `guild_configs` SET autokick = '{length}' WHERE id='{interaction.guild.id}'")
        conn.commit()
        
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        dataa = cur.fetchall()

        embed = generate_dashboard(self, data=dataa)
        await self.msg.edit(embed=embed)
        await interaction.send(embed=create_success_embed(title="Success", description="Successfully updated log channel."), ephemeral=True)