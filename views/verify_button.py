import nextcord
from nextcord.interactions import Interaction
from nextcord import Interaction
from utils.constants import PRIVACYLINK

class VerifyButton(nextcord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url=PRIVACYLINK))

    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.green, disabled=False, custom_id="verify_button")
    async def verify_button(self, button: nextcord.ui.Button, interaction: Interaction):
        pass







