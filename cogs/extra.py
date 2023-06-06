import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import time, asyncio

class BotInfoLinkButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Support Server", url="https://nomindustries.com/SV/support"))
        self.add_item(nextcord.ui.Button(label="Invite", url="https://nomindustries.com/SV/invite"))
        self.add_item(nextcord.ui.Button(label="Vote", url="https://nomindustries.com/SV/vote"))
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url="https://nomindustries.com/SV/privacy"))

class PrivacyPolicyButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url="https://nomindustries.com/SV/privacy"))

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
        embed = nextcord.Embed(title="Simple Verification Bot Information", description=f"""Ping: {round(ping)}ms
Server count: {str(len(self.client.guilds))}
Support Server: [Need some support?](https://nomindustries.com/SV/invite)
Invite: [Invite Me](https://nomindustries.com/SV/invite)
Vote: [Vote for me](https://nomindustries.com/SV/vote)
Privacy; [Privacy Policy](https://nomindustries.com/SV/privacy)""", colour=0xadd8e6)
        await msg.edit(content = " ", embed=embed, view=BotInfoLinkButton())

    @nextcord.slash_command(name="guildinfo", description="[ADMIN ONLY]", guild_ids=[1015361041024155770])
    async def _guildinfo(self, ctx:Interaction):
        await ctx.response.defer(ephemeral=True)
        if ctx.user.id == 326065974950363136:
            for i in self.client.guilds:
                await ctx.user.send(len(i.members))
                await asyncio.sleep(1)
    
    @nextcord.slash_command(name="privacy", description=f"Get the link to our privacy policy")
    async def privacy_policy(self, ctx:Interaction):
        embed = nextcord.Embed(title="Privacy Policy", description="You can find our privacy policy here: \n\nhttps://nomindustries.com/sv/privacy", colour=0xadd8e6)
        await ctx.send(embed=embed, view=PrivacyPolicyButton())


def setup(client):
    client.add_cog(Extras(client))