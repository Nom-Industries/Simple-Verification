import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from utils import check_premium, create_error_embed, PREMIUMLINK

class Premium(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_commands(name=f"manage-premium", description=f"Manage your premium membership")
    async def manage_premium(self, interaction: Interaction):
        pass

    @manage_premium(name=f"add-server", description=f"Add a server to your premium subscription")
    async def manage_premium_add_server(self, interaction: Interaction,
        guildid: str = SlashOption(
            name=f"guild",
            description=f"The ID of the guild you want to add to your premium subscription. Use /debug in your server to get the server ID",
            required = True
        )):
        await interaction.response.defer()
        if not check_premium(interaction.user.id):
            await interaction.send(embed=create_error_embed(title=f"No premium subscription", description=f"You are not currently subscribed to any of our premium subscriptions. To purchase premium please follow [this link]({PREMIUMLINK})\n\n\nPlease Note: If you recently subscribed to premium it may take up to 30 minutes to register your subscription. If you are still unable to use this command in 30 minutes, please create a ticket in "))

def setup(client: commands.Bot):
    client.add_cog(Premium(client))