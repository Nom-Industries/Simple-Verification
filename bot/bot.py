import nextcord
import os
from nextcord.ext import commands
from utils.utils import *
from utils.constants import TOKEN

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(shard_count=1, command_prefix="nom!")
        self.unloaded_cogs = []

    def initialize(self):
        self.load_extensions()
        self.run(TOKEN)
    
    def load_extensions(self):
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(name=f"cogs.{cog[:-3]}")
                    print(f"Loaded {cog[:-3]} cog")

                except Exception as e:
                    print(e)
                    print(f"Failed to load {cog[:-3]} cog")
                    self.unloaded_cogs.append(cog.capitalize()[-3])
    
    async def on_ready(self):
        print(f"Logged in as {self.user}!")
        print(self.shards)
        for shard in self.shards:
            await self.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name=f"Verifying | Shard: {shard+1}/{len(self.shards)}"), shard_id=shard)