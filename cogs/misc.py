import nextcord
from nextcord.ext import commands
import time
from nextcord import Interaction
from views import BotInfoLinkButton, PrivacyPolicyButton
import cooldowns
from utils.constants import COLOUR_MAIN, VOTELINK, INVITELINK, DISCORDLINK, PRIVACYLINK

class Misc(commands.Cog):
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


    @nextcord.slash_command(name=f"shardinfo", description=f"Get information on all shards")
    @cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
    async def shardinfo(self, interaction:Interaction):
        await interaction.response.defer()
        description = ""
        for shard in self.client.shards:
            specshard = self.client.get_shard(shard)
            shard_servers = len([guild for guild in self.client.guilds if guild.shard_id == shard])
            description+=f"\n**Shard {shard+1}** has `{round(specshard.latency*100)}ms` latency with `{shard_servers} servers`"

        if not interaction.guild:
            await interaction.send(embed=nextcord.Embed(title=f"Simple Verification Shard Information", description=f"All current shards:\n {description}", colour=COLOUR_MAIN))
        else:
            guild_shard = interaction.guild.shard_id
            guildspecshard = self.client.get_shard(guild_shard)
            guild_shard_servers = len([guild for guild in self.client.guilds if guild.shard_id == guild_shard])
            await interaction.send(f"This server's shard is shard **{guild_shard+1}** with `{round(guildspecshard.latency*100)}ms` and `{guild_shard_servers} servers`", embed=nextcord.Embed(title=f"Simple Verification Shard Information", description=f"All current shards:\n {description}", colour=COLOUR_MAIN))


    
    @nextcord.slash_command(name=f"shardinfo", description=f"Get information on all shards")
    @cooldowns.cooldown(1, 30, bucket=cooldowns.SlashBucket.author)
    async def shardinfo(self, interaction:Interaction):
        await interaction.response.defer()
        description = ""
        for shard in self.client.shards:
            specshard = self.client.get_shard(shard)
            shard_servers = len([guild for guild in self.client.guilds if guild.shard_id == shard])
            description+=f"\n**Shard {shard+1}** has `{round(specshard.latency*100)}ms` latency with `{shard_servers} servers`"

        if not interaction.guild:
            await interaction.send(embed=nextcord.Embed(title=f"Simple Verification Shard Information", description=f"All current shards:\n {description}", colour=COLOUR_MAIN))
        else:
            guild_shard = interaction.guild.shard_id
            guildspecshard = self.client.get_shard(guild_shard)
            guild_shard_servers = len([guild for guild in self.client.guilds if guild.shard_id == guild_shard])
            await interaction.send(f"This server's shard is shard **{guild_shard+1}** with `{round(guildspecshard.latency*100)}ms` and `{guild_shard_servers} servers`", embed=nextcord.Embed(title=f"Simple Verification Shard Information", description=f"All current shards:\n {description}", colour=COLOUR_MAIN))


def setup(client: commands.Bot):
    client.add_cog(Misc(client))