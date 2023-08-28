import nextcord
import json
import os
from nextcord.ext import commands , tasks
import requests
from utils.constants import TOKEN

os.chdir("./")



class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
        self = self

    async def on_ready(self):
        if not self.persistent_views_added:
            self.persistent_views_added = True

        print(f"Logged in as {client.user}!")

        await client.change_presence(status = nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="People Verify"))


intents = nextcord.Intents.default()

intents.members = True
client = Bot(command_prefix = "nom!", intents = intents)

for filename in os.listdir('./cogs'):   
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename} cog")





















client.run(TOKEN)
