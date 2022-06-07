import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import json


class HelpButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Support Server", url="https://discord.gg/aGzvXvTkP8"))
        self.add_item(nextcord.ui.Button(label="Invite", url=" https://discord.com/api/oauth2/authorize?client_id=981835181243658260&permissions=8&scope=bot%20applications.commands"))
        self.add_item(nextcord.ui.Button(label="Vote", url="https://top.gg/bot/828584622156939274/vote"))


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="help", description="Help command")
    async def help(self,
        ctx: Interaction):
        await ctx.response.defer()
        embed = nextcord.Embed(title=(f"Help"), description=(f"""Below is a list of all commands you will need:"""), colour=0xadd8e6)
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
        embed.add_field(name="\u200B", value=f"[Support Server](https://discord.gg/aGzvXvTkP8) | [Invite Me]( https://discord.com/api/oauth2/authorize?client_id=981835181243658260&permissions=8&scope=bot%20applications.commands) | [Vote](https://top.gg/bot/828584622156939274/vote)", inline=False)


        await ctx.send(embed=embed, view=HelpButtons())


def setup(client):
    client.add_cog(Help(client))