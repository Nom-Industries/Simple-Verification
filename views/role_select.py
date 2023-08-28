import nextcord
from nextcord.interactions import Interaction
from utils import *
from nextcord import Interaction

class RoleSelectDropdown(nextcord.ui.RoleSelect):
    def __init__(self, minvalue=1, maxvalue=1, text="Select a role"):
        super().__init__(custom_id="test", placeholder=text, min_values=minvalue, max_values=maxvalue)
    
    async def callback(self, interaction: Interaction):
        self.view.values = self.values
        self.view.stop()

class RoleSelect(nextcord.ui.View):
    def __init__(self, minvalue=1, maxvalue=1, text="Select a role"):
        super().__init__()
        self.add_item(RoleSelectDropdown(minvalue=minvalue, maxvalue=maxvalue, text=text))
        self.values = []

    @nextcord.ui.button(label="Remove Roles", style=nextcord.ButtonStyle.red, disabled=False)
    async def remove(self, button: nextcord.ui.Button, interaction: Interaction):
        self.values = None
        self.stop()
    