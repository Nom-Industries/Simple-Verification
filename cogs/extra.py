import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import time

class BotInfoLinkButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Support Server", url="https://discord.gg/aGzvXvTkP8"))
        self.add_item(nextcord.ui.Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=981835181243658260&permissions=8&scope=bot%20applications.commands"))
        self.add_item(nextcord.ui.Button(label="Vote", url="https://top.gg/bot/828584622156939274/vote"))


class Extras(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="botinfo", description="Shows the bot information")
    async def _botinfo(
        self,
        ctx: Interaction,
        ):
        await ctx.response.defer()
        before = time.monotonic()
        msg = await ctx.send("Loading bot information")
        ping = (time.monotonic() - before) * 1000
        embed = nextcord.Embed(title="Bot Infomation", description=f"""Ping: {round(ping)}ms
Server count: {str(len(self.client.guilds))}
Support Server: [Need some support?](https://discord.gg/aGzvXvTkP8)
Invite: [Invite Me](https://discord.com/api/oauth2/authorize?client_id=981835181243658260&permissions=8&scope=bot%20applications.commands)
Vote: [Vote for me](https://top.gg/bot/828584622156939274/vote)""", colour=0xadd8e6)
        await msg.edit(content = " ", embed=embed, view=BotInfoLinkButton())


def setup(client):
    client.add_cog(Extras(client))