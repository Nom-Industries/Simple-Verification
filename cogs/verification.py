import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, pymysql, asyncio, random, string, os, sys
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from views.answer_view import AnswerModal,AnswerButton
from views.embed_manager_views import EmbedCreationForm
import time
import io
import math
import datetime
from difflib import SequenceMatcher

verifying = []
letters = ["a ", "b ", "c ", "d ", "e ", "g ", "k ", "m ", "n ", "o ", "p ", "q ", "s ", "u ", "v ", "w ", "x ", "y ", "z "]

class BotVerifyLinks(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Invite me to your server", url="https://nomindustries.com/SV/invite"))
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url="https://nomindustries.com/SV/privacy"))


class VerifyButton(nextcord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)
        self.add_item(nextcord.ui.Button(label="Privacy Policy", url="https://nomindustries.com/SV/privacy"))
        with open('dbconfig.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]

    async def generate_captcha_string(self):
        result_str = ""
        allowed = False
        f = open("./filter/filter.txt", "r")
        lines = f.readlines()
        while not allowed:
            rangee = random.randint(4,5)
            result_str = ''.join(random.choice(letters) for i in range(rangee))
            allowed = True
            for line in lines:
                similarity = SequenceMatcher(None, (result_str.lower().replace(" ", "")), (line.strip().lower().replace(" ", "")))
                if similarity.ratio() > 0.5:
                    allowed=False

        return result_str

    @nextcord.ui.button(label='Verify', style=nextcord.ButtonStyle.green, custom_id='verify_button_view:verify')
    async def verify(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        global verifying
        if ctx.user.id in verifying:
            await ctx.send("You are already verifying. Please complete that verification to verify again", ephemeral=True)
            return
        else:
            verifying.append(ctx.user.id)
            await ctx.response.defer(with_message=True, ephemeral=True)
            conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM guild_configs WHERE id='{ctx.guild.id}'")
            data = cur.fetchall()
            if data:
                data = data[0]
                if not data[1] == None:
                    if data[4] == "0": # if captcha type is none
                        try:
                            veryroleid = data[1]
                            veryrole = ctx.guild.get_role(int(veryroleid))
                            unverifiedrole = None
                            if not data[2] == None:
                                unverifiedroleid = data[2]
                                unverifiedrole = ctx.guild.get_role(int(unverifiedroleid))
                            logchannel = None
                            if not data[3] == None:
                                logchannelid = data[3]
                                logchannel = ctx.guild.get_channel(int(logchannelid))
                            if (not veryrole in ctx.user.roles) or (unverifiedrole != None and unverifiedrole in ctx.user.roles):
                                embed =nextcord.Embed(title="Verification", description=f"{ctx.user.mention} has successfully verified", colour=0xadd8e6)
                                try:
                                    await ctx.user.add_roles(veryrole)
                                    embed.add_field(name="Roles added", value=f"{veryrole.mention}")
                                    if not unverifiedrole == None and unverifiedrole in ctx.user.roles:
                                        try:
                                            await ctx.user.remove_roles(unverifiedrole)
                                            embed.add_field(name="Roles removed", value=f"{unverifiedrole.mention}")
                                        except:
                                            await ctx.send("Failed to remove unverified role.", ephemeral=True)
                                            embed.add_field(name="Roles removed", value=f"Failed to remove unverified role")
                                            index = verifying.index(ctx.user.id)
                                            del verifying[index]
                                            if not logchannel == None:
                                                try:
                                                    await logchannel.send(embed=embed)
                                                except:
                                                    pass
                                            return
                                except Exception as e:
                                    print(e)
                                    await ctx.send("Failed to add verified role", ephemeral=True)
                                    embed.add_field(name="Roles added", value=f"Failed to give verified role")
                                    index = verifying.index(ctx.user.id)
                                    del verifying[index]
                                    if not logchannel == None:
                                        try:
                                            await logchannel.send(embed=embed)
                                        except:
                                            pass
                                    return

                                await ctx.send(f"You have successfully verified", ephemeral=True, view=BotVerifyLinks())
                                
                                if not logchannel == None:
                                    try:
                                        await logchannel.send(embed=embed)
                                    except:
                                        pass
                                        

                            else:
                                await ctx.send("You are already verified", ephemeral=True, view=BotVerifyLinks())
                    
                        except Exception as e:
                            print(e)
                            await ctx.send("Server config not setup properly, contact the server admins to fix this.", ephemeral=True)
                        
                        

                    
                    elif data[4] == "2":
                        try:
                            veryroleid = data[1]
                            veryrole = ctx.guild.get_role(int(veryroleid))
                            unverifiedrole = None
                            if not data[2] == None:
                                unverifiedroleid = data[2]
                                unverifiedrole = ctx.guild.get_role(int(unverifiedroleid))
                            logchannel = None
                            if not data[3] == None:
                                logchannelid = data[3]
                                logchannel = ctx.guild.get_channel(int(logchannelid))
                            if (not veryrole in ctx.user.roles) or (unverifiedrole != None and unverifiedrole in ctx.user.roles):
                                result_str = await self.generate_captcha_string()
                                image = ImageCaptcha(width = 280, height = 90, fonts=["nom.ttf", "GolosText-Regular.ttf", "NotoSerif-Regular.ttf", "Poppins-Regular.ttf", "Roboto-Regular.ttf", "SourceSansPro-Regular.ttf"], font_sizes=[60])
                                data = image.generate(result_str.lower())
                                bytes = io.BytesIO()
                                image.write(result_str, bytes)
                                bytes.seek(0)
                                embed=nextcord.Embed(title=(f"Captcha"), description=(f"""You have 1 minute to answer the captcha correctly. 
                                                                                
The captcha will only be **under case** **letters**.
If you get it wrong just click the verify button again and retry"""), colour=0xadd8e6)
                                try:
                                    answerview = AnswerButton(actual_answer=result_str)
                                    msg = await ctx.send(embed=embed, file=nextcord.File(bytes, f"{ctx.user.id}-captcha.jpg"), ephemeral=True)
                                    logembed=nextcord.Embed(title=f"Verification Started", description=f"{ctx.user.mention} started verification with the captcha attached. The answer to the captcha is `{str(result_str).replace(' ', '')}`", colour=0xadd8e6)
                                    logembed.set_author(name=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar else None)
                                    logembed.set_image(url=msg.attachments[0].url)
                                    try:
                                        logmsg = await logchannel.send(embed=logembed)
                                    except Exception as e:
                                        print(e)
                                        pass
                                    await msg.edit(view=answerview)
                                    await answerview.wait()
                                    result_str = result_str.replace(" ", "")
                                    answer = answerview.answer
                                    await msg.delete()
                                    if answer == "Too Long ---------------":
                                        await ctx.send("You ran out of time to answer the captcha, please try again.", ephemeral=True)
                                        index = verifying.index(ctx.user.id)
                                        del verifying[index]
                                        logembed=nextcord.Embed(title=f"Verification Failed", description=f"{ctx.user.mention} failed verification with the captcha attached. The answer to the captcha is `{result_str}` but they didn't answer in time.", colour=0xff0000)
                                        logembed.set_author(name=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar else None)
                                        try:
                                            await logmsg.reply(embed=logembed)
                                        except:
                                            pass
                                        return
                                    if answer.lower() == result_str:
                                        embed =nextcord.Embed(title="Verification", description=f"{ctx.user.mention} has successfully verified", colour=0x00ff00)
                                        try:
                                            await ctx.user.add_roles(veryrole)
                                            embed.add_field(name="Roles added", value=f"{veryrole.mention}")
                                            if not unverifiedrole == None and unverifiedrole in ctx.user.roles:
                                                try:
                                                    await ctx.user.remove_roles(unverifiedrole)
                                                    embed.add_field(name="Roles removed", value=f"{unverifiedrole.mention}")
                                                except:
                                                    await ctx.send("Failed to remove unverified role.", ephemeral=True)
                                                    embed.add_field(name="Roles removed", value=f"Failed to remove unverified role")
                                                    index = verifying.index(ctx.user.id)
                                                    del verifying[index]
                                                    if not logchannel == None:
                                                        try:
                                                            await logmsg.reply(embed=embed)
                                                        except:
                                                            pass
                                                    return
                                        except Exception as e:
                                            print(e)
                                            await ctx.send("Failed to add verified role", ephemeral=True)
                                            embed.add_field(name="Roles added", value=f"Failed to give verified role")
                                            index = verifying.index(ctx.user.id)
                                            del verifying[index]
                                            if not logchannel == None:
                                                try:
                                                    await logmsg.reply(embed=embed)
                                                except:
                                                    pass
                                            return
                                        await ctx.send(f"You have successfully verified", ephemeral=True, view=BotVerifyLinks())
                                        
                                        if not logchannel == None:
                                            try:
                                                await logmsg.reply(embed=embed)
                                            except:
                                                pass
                                    else:
                                        await ctx.send(f"Incorrect answer, please try again. Correct answer was `{result_str}`", ephemeral=True)
                                        logembed=nextcord.Embed(title=f"Verification Failed", description=f"{ctx.user.mention} failed verification with the captcha attached. The answer to the captcha is `{result_str}` but their answer was `{answer}`", colour=0xff0000)
                                        logembed.set_author(name=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar else None)
                                        try:
                                            await logmsg.reply(embed=logembed)
                                        except:
                                            pass

                                except Exception as e:
                                    print(e)
                                    await ctx.send("Error sending captcha", ephemeral=True)
                                    try:
                                        os.remove(f"{ctx.user.id}-captcha.jpg")
                                    except:
                                        pass
                            else:
                                await ctx.send("You are already verified", ephemeral=True, view=BotVerifyLinks())
                        except Exception as e:
                            print(e)
                            await ctx.send("Server config not setup properly, contact the server admins to fix this.", ephemeral=True)

                try:
                    index = verifying.index(ctx.user.id)
                    del verifying[index]
                
                except:
                    pass

            else:
                await ctx.send("Server config not setup properly, contact the server admins to fix this.")
                index = verifying.index(ctx.user.id)
                del verifying[index]
            
        

class VerifyMessage(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open('dbconfig.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]

    @nextcord.slash_command(name="verifymessage", description="Send the verification message to a channel")
    async def verifymessage(self,
        ctx: Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="Channel to send verification message to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        ),
        custom: bool = SlashOption(
            name="custom",
            description="Choose to send a custom embed",
            required=False
        )):
        client = self.client
        if ctx.user.guild_permissions.administrator == True:
            if custom:
                options = EmbedCreationForm()
                await ctx.response.send_modal(modal=options)
                await options.wait()
                embed = nextcord.Embed(title=options.embedtitle, description=options.embeddescription, colour=0xadd8e6)
            else:
                embed=nextcord.Embed(title=f"Verification", description=f"To verify in the server press the button below and follow the instructions from there.", colour=0xadd8e6)
            try:
                await channel.send(embed=embed, view=VerifyButton(self.client))
                await ctx.send(f"Message sent to {channel.mention}")
            except Exception as e:
                print(e)
                try:
                    await ctx.send("Error sending message. Make sure I have permission to send messages and embed links in the selected channel.")
                except:
                    pass
        else:
            await ctx.send("You require `administrator` permissions to perform this command", ephemeral=True)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        global verifying
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{member.guild.id}'")
        data = cur.fetchall()
        if data:
            data = data[0]
            if not data[1] == None:
                now = datetime.datetime.now(datetime.timezone.utc)
                secs = (now - member.created_at).days
                kicked = False
                if data[5] == "0":
                    pass
                else:
                    days = int(data[5])
                    if secs < days:
                        try:
                            await member.send(f"You were kicked from **{member.guild.name}** due to your account age being below their limit of **{days} days**")
                        except:
                            pass
                        await member.kick(reason=f"Account age below server limit of {days} days")
                        index = verifying.index(member.id)
                        del verifying[index]
            if not data[2] == None:
                role = member.guild.get_role(int(data[2]))
                await member.add_roles(role)
            



def setup(client):
    client.add_cog(VerifyMessage(client))
                    
