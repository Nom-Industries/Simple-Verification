import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import check_premium, DBENDPOINT, DBNAME, DBPASS, DBUSER, generate_dashboard, create_warning_embed
from views import DashboardButtons
import pymysql

class Dashboard(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name=f"dashboard", description=f"Configure the bot on the in-discord dashboard")
    async def dashboard(self, interaction: Interaction):
        interaction.response.defer(with_message=True, ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.send(embed=create_warning_embed(title="Insufficient permissions", description="You need the `administrator` permission to use this."))
            return
        
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            cur.execute(f"INSERT INTO guild_configs (id) VALUES ('{interaction.guild.id}')")
            conn.commit()
            
        embed = generate_dashboard(data=data)
        view = DashboardButtons(premium=check_premium(self, guild = True, user = False, type_id=interaction.guild.id))
        await interaction.send(embed=embed, view=view, ephemeral=True)

def setup(client: commands.Bot):
    client.add_cog(Dashboard(client))