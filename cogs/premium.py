import nextcord
import pymysql
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from utils import check_premium, create_error_embed, create_warning_embed, PREMIUMLINK, DBENDPOINT, DBUSER, DBPASS, DBNAME

class Premium(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name=f"manage-premium", description=f"Manage your premium membership", guild_ids=[1111387758028652657, 801744339343507457])
    async def manage_premium(self, interaction: Interaction):
        pass

    @manage_premium.subcommand(name=f"add-server", description=f"Add a server to your premium subscription")
    async def manage_premium_add_server(self, interaction: Interaction,
        guildid: str = SlashOption(
            name=f"guild",
            description=f"The ID of the guild to add to premium. Use /debug in your server to get this.",
            required = True
        )):
        await interaction.response.defer()
        if not check_premium(False, True, interaction.user.id):
            await interaction.send(embed=create_error_embed(title=f"No premium subscription", description=f"You are not currently subscribed to any of our premium subscriptions. To purchase premium please follow [this link]({PREMIUMLINK})\n\n\nPlease Note: If you recently subscribed to premium it may take up to 30 minutes to register your subscription. If you are still unable to use this command in 30 minutes, please create a ticket in "))
            return

        if check_premium(True, False, guildid):
            await interaction.send(embed=create_warning_embed(title=f"Guild already added", description=f"This guild is already added to your premium subscription."))
            return
        
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sv_premium_users WHERE user_id = %s", (interaction.user.id))
        data = cur.fetchall()

        servers_available = int(data[0][1])

        cur.execute("SELECT * FROM sv_premium_guilds WHERE user_id = %s", (interaction.user.id))
        data = cur.fetchall()

        servers_used = len(data) if data else 0


    

def setup(client: commands.Bot):
    client.add_cog(Premium(client))