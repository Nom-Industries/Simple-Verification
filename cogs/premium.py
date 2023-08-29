import nextcord
import pymysql
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from utils import check_premium, create_error_embed, create_warning_embed, create_success_embed, PREMIUMLINK, DBENDPOINT, DBUSER, DBPASS, DBNAME

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
        if not check_premium(self, False, True, interaction.user.id):
            await interaction.send(embed=create_error_embed(title=f"No premium subscription", description=f"You are not currently subscribed to any of our premium subscriptions. To purchase premium please follow [this link]({PREMIUMLINK})\n\n\nPlease Note: If you recently subscribed to premium it may take up to 30 minutes to register your subscription. If you are still unable to use this command in 30 minutes, please create a ticket in <#1111392014529990656>"))
            return

        if check_premium(self, True, False, guildid):
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

        if servers_available <= servers_used:
            await interaction.send(embed=create_warning_embed(title=f"Max Servers Reached", description=f"You have reached the limit of premium servers that your current premium subscription allows for (``{servers_available}``). To increase this limit, upgrade your premium subscription via [this link]({PREMIUMLINK})"))
            return
        
        try:
            guild = self.get_guild(int(guildid))
        except:
            await interaction.send(embed=create_error_embed(title=f"Invalid guild ID", description=f"You have given an invalid guild ID. Please use the `/debug` command in the guild you want to add premium to to get the correct guild ID."))
            return
        
        cur.execute("INSERT INTO sv_premium_guilds VALUES (user_id, guild_id) SET (%s, %s)", (interaction.user.id, guildid))
        conn.commit()

        await interaction.send(embed=create_success_embed(title=f"Premium server added", description=f"You have succesfully given `{guild.name} ({guild.id})` to your premium subscription."))
        



    @tasks.loop(minutes=5)
    async def premium_manager(self):
        premium_role_ids = [1130511638794080419, 1130520156477608036, 1130520224689557554, 1130520278850613369, 1130520336744591431] # ACTUAL IDS = [1130511638794080419, 1130520156477608036, 1130520224689557554, 1130520278850613369, 1130520336744591431]
        guild = self.get_guild(1111387758028652657) # ACTUAL ID = 1111387758028652657
        premium_roles = [].append([role for role in guild.get_role([roleid for roleid in premium_role_ids])])

        print(premium_roles)

        for member in guild.members:
            if premium_role_ids in member.roles:
                pass

def setup(client: commands.Bot):
    client.add_cog(Premium(client))