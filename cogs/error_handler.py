import nextcord
from cooldowns import CallableOnCooldown
from nextcord.ext import commands, application_checks
from bot.bot import Bot
from nextcord.errors import Forbidden
from utils import *
import time

class Error_handler(commands.Cog):
    def init(self, client: Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction:nextcord.Interaction, error):
        error = getattr(error, "original", error)
        if isinstance(error, CallableOnCooldown):
            await interaction.send(f"That command is on cooldown. You can use it again <t:{int(error.retry_after) + round(int(time.time()))}:R>")
        elif isinstance(error, Forbidden):
            await interaction.send(f"I don't have permission to do that")
        else:
            raise error

def setup(client: Bot):
    client.add_cog(Error_handler(client))