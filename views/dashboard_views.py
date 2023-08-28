import nextcord, pymysql
from utils import DBENDPOINT, DBNAME, DBPASS, DBUSER, COLOUR_MAIN, create_error_embed, DISCORDLINK
from nextcord import Interaction
from .role_select import RoleSelect

class DashboardButtons(nextcord.ui.View):
    def __init__(self, premium: bool = False):
        super().__init__(timeout=300)
        self.premium = premium

    @nextcord.ui.Button(label="Set Verification Roles", style=nextcord.ButtonStyle.blurple, disabled=False)
    async def set_verification_role(self, interaction: Interaction, button: nextcord.ui.Button):
        await interaction.response.defer(with_message=True, ephemeral=True)
        if self.premium:
            rselect = RoleSelect(minvalue=1, maxvalue=10, text="Select Verification Roles")
            embed = nextcord.Embed(title="Select Verification Roles", description="Select the role you want members to recieve when they verify. \nAs a [premium]({PREMIUMLINK}) user you can select up to `10` roles!", color=COLOUR_MAIN)
        else:
            rselect = RoleSelect(minvalue=1, maxvalue=1, text="Select Verification Roles")
            embed = nextcord.Embed(title="Select Verification Roles", description="Select the role you want members to recieve when they verify. \nAs a standard user you can select `1` role. \nUpgrade to [premium]({PREMIUMLINK}) to be able to select up to `10` roles!", color=COLOUR_MAIN)
        
        msg = await interaction.send(embed=embed, view=rselect, ephemeral=True)
        await rselect.wait()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            await msg.edit(embed=create_error_embed(title="Error!", description=f"Failed to fetch your guild data, please report this in our [Support Server]({DISCORDLINK})"), view=None)
            self.stop()
            return
        
        for role in rselect.values:
            ",".join(role.id)