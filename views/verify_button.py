import nextcord, pymysql, io
from nextcord.interactions import Interaction
from nextcord import Interaction
from utils import PRIVACYLINK, create_warning_embed, DBENDPOINT, DBNAME, DBPASS, DBUSER, COLOUR_MAIN, create_error_embed, generate_random_string, COLOUR_BAD, COLOUR_GOOD
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from views import AnswerButton

verifying = []
letters = ["a ", "b ", "c ", "d ", "e ", "g ", "k ", "m ", "n ", "o ", "p ", "q ", "s ", "u ", "v ", "w ", "x ", "y ", "z "]

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
        if not data:
            await interaction.send(embed=create_error_embed(title=f"Invalid Configuration", description=f"This server has an invalid configuration. Please contact the server administrator to fix this issue."))
            return
        data = data[0]
        if not data[1]:
            await interaction.send(embed=create_error_embed(title=f"Invalid Configuration", description=f"This server has an invalid configuration (no verified role set). Please contact the server administrator to fix this issue."))
            return
        
        verifiedrole = interaction.guild.get_role(int(data[1]))
        unverifiedrole = None
        if data[2]:
            unverifiedrole = interaction.guild.get_role(int(data[2]))

        captcha_str = generate_random_string(int(data[7], int(data[8])))
        captcha = ImageCaptcha(width = 280, height = 90, fonts=["./assets/nom.ttf", "./assets/GolosText-Regular.ttf", "./assets/NotoSerif-Regular.ttf", "./assets/Poppins-Regular.ttf", "./assets/Roboto-Regular.ttf", "./assets/SourceSansPro-Regular.ttf"], font_sizes=[60])
        data = captcha.generate(generate_random_string(captcha_str))
        bytes = io.BytesIO()
        captcha.write(captcha_str, bytes)
        bytes.seek(0)
        embed=nextcord.Embed(title=f"Captcha", description=f"You have **1 minute** to answer the captcha correctly.\n\n\nThe captcha will only be **undercase letters**.\nIf you get the captcha wrong, just click the verify button again and retry.", colour=COLOUR_MAIN)
        answerview = AnswerButton(actual_answer=captcha_str)
        msg = await interaction.send(embed=embed, file=nextcord.File(bytes, f"captcha.jpg", ephemeral=True))
        logembed = nextcord.Embed(title=f"Verification Started", description=f"{interaction.user.mention} started verification with the captcha attached. The answer to the captcha is `{str(captcha_str).replace(' ', '')}`", colour=COLOUR_GOOD)
        logembed.set_author(name=f"{interaction.user.replace('#0', '')}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        logembed.set_image(url=msg.attachments[0].url)
        try:
            if data[3]:
                logchannel = interaction.guild.get_channel(int(data[3]))
                logmsg = await logchannel.send(embed=logembed)
            else:
                logchannel = False
        except:
            pass

        await msg.edit(view=answerview)
        await answerview.wait()
        answer_str = captcha_str.replace(" ", "")
        await msg.delete()
        answer = answerview.answer
        if answer == "Too Long ---------------":
            embed=nextcord.Embed(title="Time limit exceeded", description=f"You have exceeded the 60 second time limit. Please try again.")
            del verifying[verifying.index(interaction.user.id)]
            logembed.title=f"Verification Failed"
            logembed.description=f"{interaction.user.mention} exceeded the 60 second time limit."
            logembed.colour=COLOUR_BAD
            if logchannel:
                try:
                    logmsg.edit(embed=logembed)
                except:
                    pass
            return
        elif answer.lower() == answer_str:
            logembed.title=f"Verification Succeeded"
            logembed.description=f"{interaction.user.mention} has successfully verified."
            logembed.colour=COLOUR_GOOD
            try:
                verifiedrole = 
                await interaction.user.add_roles()
        
