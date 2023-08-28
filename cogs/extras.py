import nextcord
from nextcord.ext import commands
import time
from nextcord import Interaction
from views import BotInfoLinkButton, PrivacyPolicyButton
from utils.constants import COLOUR_MAIN, VOTELINK, INVITELINK, DISCORDLINK, PRIVACYLINK

class Extras(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name="botinfo", description="Information about the bot")
    async def botinfo(self, interaction: Interaction):
        await interaction.response.defer()
        before = time.monotonic()
        msg = await interaction.send("Loading bot information")
        ping = (time.monotonic() - before) * 1000
        users = 0
        for guild in self.client.guilds:
            users+=guild.member_count
        embed = nextcord.Embed(title="Bot Infomation", description=f"""Ping: {round(ping)}ms
Server count: {str(len(self.client.guilds))}
User count: {users:,}
Support Server: [Need some support?]({DISCORDLINK})
Invite: [Invite Me]({INVITELINK})
Vote: [Vote for me]({VOTELINK})
Privacy: [Privacy Policy]({PRIVACYLINK})""", colour=COLOUR_MAIN)
        await msg.edit(content = " ", embed=embed, view=BotInfoLinkButton())

    @nextcord.slash_command(name=f"privacy", description=f"Get the link to our privacy policy")
    async def privacy(self, interaction:Interaction):
        await interaction.send(content="", view=PrivacyPolicyButton())

def setup(client: commands.Bot):
    client.add_cog(Extras(client))