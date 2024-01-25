import nextcord, pymysql, io, random
from nextcord.interactions import Interaction
from assets import *
from utils import PRIVACYLINK, create_warning_embed, DBENDPOINT, DBNAME, DBPASS, DBUSER, COLOUR_BAD, COLOUR_GOOD
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
async def get_verified_role(guild, data):
    if not data[1]:
        return None
    return await guild.get_role(int(data[1]))

@staticmethod
async def get_unverified_role(guild, data):
    if not data[2]:
        return None
    return await guild.get_role(int(data[2]))

@staticmethod
async def add_verified_role(guild, user, data):
    verifiedrole = await get_verified_role(guild, data)
    if not verifiedrole:
        return None
    try:
        await user.add_roles(verifiedrole)
        return True
    except:
        return False

@staticmethod
async def remove_unverified_role(guild, user, data):
    unverifiedrole = await get_unverified_role(guild, data)
    if not unverifiedrole:
        return None
    try:
        await user.remove_roles(unverifiedrole)
        return True
    except:
        return False


@staticmethod
async def generate_started_log_embed(user, captcha_str, captcha_image):
    embed = nextcord.Embed(title="Verification Started", description=f"{user.mention} started verification with the captcha attached. The answer to the captcha is `{str(captcha_str).replace(' ', '')}`", colour=COLOUR_GOOD)
    embed.set_author(name=f"{user.replace('#0', '')}", icon_url=user.avatar.url if user.avatar else None)
    embed.set_image(url=captcha_image)
    return embed


@staticmethod
async def generate_captcha_string(min_length, max_length):
    return "".join(random.choice(letters) for _ in range(random.randint(min_length, max_length)))

@staticmethod
async def generate_captcha_image(min_length, max_length):
    answer_string = await generate_captcha_string(min_length, max_length)
    image =  ImageCaptcha(width=280, height=90, fonts=["nom.ttf", "GolosText-Regular.ttf", "NotoSerif-Regular.ttf", "Poppins-Regular.ttf", "Roboto-Regular.ttf", "SourceSansPro-Regular.ttf"], font_sizes=[60])
    data = image.generate(answer_string.lower())
    bytes = io.BytesIo()
    image.write(answer_string, bytes)
    bytes.seek(0)
    return bytes, answer_string

class VerifyButton(nextcord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url=PRIVACYLINK))

    @nextcord.ui.button(label="Verify", style=nextcord.ButtonStyle.green, disabled=False, custom_id="verify_button")
    async def verify_button(self, button: nextcord.ui.Button, interaction: Interaction):
        if interaction.user.id in verifying:
            await interaction.send(embed=create_warning_embed(title="Already verifying", description="You are already verifying on Simple Verification. Please complete that verification to start a new one."), ephemeral=True)
            return
        verifying.append(interaction.user.id)
        await interaction.response.defer(with_message=True, ephemeral=True)
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data or not data[1]:
            await interaction.send(embed=create_warning_embed(title="Setup not complete", description="The bot is not properly configured in this server. Please talk to the server administrators to resolve this issue. (Think this is a mistake? Reach out to our support server [here](DISCORDLINK)!)"), ephemeral=True)
            return
        
        min_captcha_length = int(data[7])
        max_captcha_length = int(data[8])

        embed = nextcord.Embed(title="Captcha", description="You have 1 minute to complete the captcha attached. The captcha will only user **undercase** **letters**.")
        captcha, answer_string = generate_captcha_image(min_captcha_length, max_captcha_length)
        answerview = AnswerButton(actual_answer=answer_string)
        msg = await interaction.send(embed=embed, file=nextcord.File(captcha, "captcha.jpg"), ephemeral=True)
        embed=generate_started_log_embed(interaction.user.id, answer_string, msg.attachments[0].url)
        logmsg = await send_to_log_channel(guild=interaction.guild, embed=embed, data=data)
        await answerview.wait()

        if answerview.answer == "Too Long ---------------":
            await msg.delete()
            await interaction.send(embed=nextcord.Embed(title="Captcha Failed", description=f"You failed the captcha because you ran out of time. Please press the verify button to try again.", colour=COLOUR_BAD))
            return
        
        if not answerview.answer.lower() == answer_string.lower():
            await msg.delete()
            await interaction.send(embed=nextcord.Embed(title=f"Captcha Failed", description=f"You failed the captcha because you got the answer wrong. Please press the verify button to try again.", colour=COLOUR_BAD))
            return
        
        error_embed = nextcord.Embed(title="Configuration Error", description="Your servers verified or unverified roles are not setup correctly. Please ensure I have the `manage_roles` permission and my highest role is **above** any of the roles you are attempting to give to users.", colour=COLOUR_BAD)
        logembed = nextcord.Embed(title="Captcha Passed", description=f"{interaction.user.mention} has passed their captcha")


        status = await remove_unverified_role(guild=interaction.guild, user=interaction.user, data=data)
        if status == False:
            await interaction.send(embed=create_warning_embed(title="Setup not complete", description="The bot is not properly configured in this server. Please talk to the server administrators to resolve this issue. (Think this is a mistake? Reach out to our support server [here](DISCORDLINK)!)"), ephemeral=True)
            await logmsg.reply(embed=error_embed)
            return
        
        status = await add_verified_role(guild=interaction.guild, user=interaction.user, data=data)
        if status == False or status == None:
            await interaction.send(embed=create_warning_embed(title="Setup not complete", description="The bot is not properly configured in this server. Please talk to the server administrators to resolve this issue. (Think this is a mistake? Reach out to our support server [here](DISCORDLINK)!)"), ephemeral=True)
            await logmsg.reply(embed=error_embed)
            return
        
        await msg.delete()
        await interaction.send(embed=nextcord.Embed(title="Captcha Passed", description=f"You have successfully passed the captcha and now have access to the server.", colour=COLOUR_GOOD))
        logembed = nextcord.Embed(title="Captcha Passed", description=f"{interaction.user.mention} has passed their captcha and thri roles have been updated.")
        await logmsg.reply(embed=logembed)
        
        
