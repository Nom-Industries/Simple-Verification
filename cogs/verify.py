import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import check_premium, DBENDPOINT, DBNAME, DBPASS, DBUSER, generate_dashboard, create_warning_embed
from views import DashboardButtons, VerifyButton
import pymysql

class Verify(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command()
    async def verify(self, interaction: Interaction):
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

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.client.add_view(VerifyButton(self.client))
            print("Loaded VerifyButton view")
        except Exception as e:
            print(e)
            print("Failed to load VerifyButton view")


def setup(client):
    client.add_cog(Verify(client))