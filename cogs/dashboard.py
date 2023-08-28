import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils import check_premium, DBENDPOINT, DBNAME, DBPASS, DBUSER
from views import DashboardButtons
import pymysql

class Dashboard(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name=f"dashboard", description=f"Configure the bot on the in-discord dashboard")
    async def dashboard(self, interaction: Interaction):
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            cur.execute(f"INSERT INTO guild_configs (id) VALUES ('{interaction.guild.id}')")
            conn.commit()
        embed = nextcord.Embed(title=f"Verification Dashboard", description=f"""Verified Role: {(",".join([('<@&' + i + '> ') for i in data[0][1].split(",")])) if data[0][1] else 'Not Set'}""")
        view = DashboardButtons(premium=check_premium(self, guild = True, user = False, type_id=interaction.guild.id))
        await interaction.send(embed=embed, view=view)

def setup(client: commands.Bot):
    client.add_cog(Dashboard(client))