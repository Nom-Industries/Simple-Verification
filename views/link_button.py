import nextcord
from utils.constants import VOTELINK, INVITELINK, DISCORDLINK, PRIVACYLINK

class BotInfoLinkButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Support Server", url=DISCORDLINK))
        self.add_item(nextcord.ui.Button(label="Invite", url=INVITELINK))
        self.add_item(nextcord.ui.Button(label="Vote", url=VOTELINK))
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url=PRIVACYLINK))



class PrivacyPolicyButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url=PRIVACYLINK))