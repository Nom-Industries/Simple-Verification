import nextcord

class EmbedCreator(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Embed Creator", timeout=600)
        self.embedtitle = nextcord.ui.TextInput(
            label="What do you want the embed title to be?",
            placeholder="You can use up to 256 characters here!",
            style=nextcord.TextInputStyle.short,
            min_length=1,
            max_length=256,
            required=True
        )
        self.embeddesc = nextcord.ui.TextInput(
            label="What do you want the embed description to be?",
            placeholder="Tip: To mention channels dp <#channel_id> (e.g. <#1111390004783091762>)",
            style=nextcord.TextInputStyle.paragraph,
            min_length=0,
            max_length=4000,
            required=False
        )
        
        self.add_item(self.embedtitle)
        self.add_item(self.embeddesc)


    async def callback(self, interaction:nextcord.Interaction):
        self.embedtitle = self.embedtitle.value
        self.embeddesc = self.embeddesc.value
        self.stop()