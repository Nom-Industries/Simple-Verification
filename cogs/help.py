import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from utils.constants import COLOUR_MAIN, VOTELINK, INVITELINK, DISCORDLINK, PRIVACYLINK
from views import BotInfoLinkButton

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name=f"help", description=f"Help command")
    async def help(self, interaction: Interaction):
        await interaction.response.defer()
        embed = nextcord.Embed(title=(f"Help"), description=(f"""Below is a list of all commands you will need:"""), colour=COLOUR_MAIN)
        embed.add_field(name=f"/config enable", value=f"""Explanation: Enable any settings you want to
Requires: Administrator
Usage: ``/config enable``""")
        embed.add_field(name=f"/config disable", value=f"""Explanation: Disable any settings you want to
Requires: Administrator
Usage: ``/config disable``""")
        embed.add_field(name=f"/verifymessage", value=f"""Explanation: Send a verification message to a channel
Requires: Administrator
Usage: ``/verifymessage <#channel> [Custom (True/False)]``""")
        embed.add_field(name=f"/botinfo", value=f"""Explanation: Shows general bot info
Requires: None
Usage: ``/botinfo``""")
        embed.add_field(name="\u200B", value=f"[Support Server]({DISCORDLINK}) | [Invite Me]({INVITELINK}) | [Vote]({VOTELINK}) | [Privacy Policy]({PRIVACYLINK})", inline=False)

        await interaction.send(embed=embed, view=BotInfoLinkButton())
    
def setup(client: commands.Bot):
    client.add_cog(Help(client))