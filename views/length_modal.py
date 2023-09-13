import nextcord
from nextcord.interactions import Interaction
from nextcord import Interaction

class LengthModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Set account age", timeout=None)

        self.length = nextcord.ui.TextInput(
                label = "How old should accounts be (in days)",
                placeholder = "To disable autokick put 0",
                style=nextcord.TextInputStyle.short,
                min_length=1,
                max_length=3,
                required=True
            )
        
        self.add_item(self.length)

    async def callback(self, interaction: nextcord.Interaction):
        self.age = self.length.value
        self.stop()

class CaptchaLengthModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Set captcha limitation", timeout=None)

        self.length = nextcord.ui.TextInput(
                label = "What do you want to set the captcha limit to?",
                placeholder = "",
                style=nextcord.TextInputStyle.short,
                min_length=1,
                max_length=3,
                required=True
            )
        
        self.add_item(self.length)

    async def callback(self, interaction: nextcord.Interaction):
        self.captcha_length = self.length.value
        self.stop()