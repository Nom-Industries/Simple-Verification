import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import pymysql, json

class GuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        supguild = self.client.get_guild(1111387758028652657)
        channel =  supguild.get_channel(1111394323720847500)
        embed = nextcord.Embed(title=f"Joined Guild", colour=0x03C04A)
        embed.add_field(name=f"Guild Name (ID)", value=f"{guild.name} ({guild.id})")
        embed.add_field(name=f"Guild Owner", value=f"{guild.owner} (<@{guild.owner.id}>)")
        embed.add_field(name=f"Guild Members", value=f"{len(guild.members)}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        supguild = self.client.get_guild(1111387758028652657)
        channel =  supguild.get_channel(1111394323720847500)
        embed = nextcord.Embed(title=f"Left Guild", colour=0x900D09)
        embed.add_field(name=f"Guild Name (ID)", value=f"{guild.name} ({guild.id})")
        embed.add_field(name=f"Guild Owner", value=f"{guild.owner} (<@{guild.owner.id}>)")
        embed.add_field(name=f"Guild Members", value=f"{len(guild.members)}")
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(cog=GuildJoin(client=client))