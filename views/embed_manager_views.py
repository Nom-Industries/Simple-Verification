from asyncio import tasks
import nextcord, pymysql
from nextcord.ext import commands


class EmbedCreationForm(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Embed Create", timeout=None)
        self.embedtitle = nextcord.ui.TextInput(
                label = "What do you want the title to be?",
                placeholder = "Tip: Up to 256 characters!",
                style=nextcord.TextInputStyle.short,
                min_length=1,
                max_length=256,
                required=True
            )
        self.add_item(self.embedtitle)

        self.embeddescription = nextcord.ui.TextInput(
                label = "What do you want the description to be?",
                placeholder = "Tip: To mention channels do <#channelid> (eg. <#1028741186380365865>)",
                style=nextcord.TextInputStyle.paragraph,
                min_length=1,
                max_length=4000,
                required=True
            )
        self.add_item(self.embeddescription)


    async def callback(self, interaction: nextcord.Interaction):
        self.embeddescription = self.embeddescription.value
        self.embedtitle = self.embedtitle.value
        self.stop()