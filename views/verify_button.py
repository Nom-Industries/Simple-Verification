import nextcord, pymysql, io
from nextcord.interactions import Interaction
from nextcord import Interaction
from utils import PRIVACYLINK, create_warning_embed, DBENDPOINT, DBNAME, DBPASS, DBUSER, COLOUR_MAIN, create_error_embed, generate_random_string, COLOUR_BAD, COLOUR_GOOD
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from views import AnswerButton

verifying = []
letters = ["a ", "b ", "c ", "d ", "e ", "g ", "k ", "m ", "n ", "o ", "p ", "q ", "s ", "u ", "v ", "w ", "x ", "y ", "z "]

@staticmethod
async def get_log_channel(guild, data):
    if not data[3]:
        return None
    return await guild.get_channel(int(data[3]))

@staticmethod
async def send_to_log_channel(guild, embed, data):
    logchannel = await get_log_channel(guild, data)
    if not logchannel:
        return None
    msg = await logchannel.send(embed=embed)
    return msg

@staticmethod
async def generate_started_embed(user, captcha_str, captcha_image):
    embed = nextcord.Embed(title=f"Verification Started", description=f"{user.mention} started verification with the captcha attached. The answer to the captcha is `{str(captcha_str).replace(' ', '')}`", colour=COLOUR_GOOD)
    embed.set_author(name=f"{user.replace('#0', '')}", icon_url=user.avatar.url if user.avatar else None)
    embed.set_image(url=captcha_image)
    return embed

@staticmethod
async def generate_fail_embed(user, embed, fail_type, captcha_str):
    embed.title = "Verification Failed"
    embed.description = f"{user.mention} exceeded the 60 second time limit. The answer to the captcha was {captcha_str}." if fail_type == "time" else f"{user.mention} failed the captcha. The correct answer to the captcha was {captcha_str}."
    embed.colour = COLOUR_BAD
    return embed

@staticmethod

class VerifyButton(nextcord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url=PRIVACYLINK))

    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.green, disabled=False, custom_id="verify_button")
    async def verify_button(self, button: nextcord.ui.Button, interaction: Interaction):
        global verifying
        if interaction.user.id in verifying:
            await interaction.send(embed=create_warning_embed(title=f"Already verifying", description=f"You are already verifying on Simple Verification. Please complete that verification to start a new one."), ephemeral=True)
            return
        verifying.append(interaction.user.id)
        await interaction.response.defer(with_message=True, ephemeral=True)
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        
