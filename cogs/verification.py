import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, pymysql, asyncio, random, string, os, sys
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
import time
import math
import datetime

verifying = []
letters = ["a ", "b ", "c ", "d ", "e ", "g ", "k ", "m ", "n ", "o ", "p ", "q ", "s ", "u ", "v ", "w ", "x ", "y ", "z "]







class VerifyButton(nextcord.ui.View):
    def __init__(self, client):
        self.client = client
        super().__init__(timeout=None)
        with open('dbconfig.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]

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

                                await ctx.send(f"You have successfully verified", ephemeral=True)
                                
                                if not logchannel == None:
                                    try:
                                        await logchannel.send(embed=embed)
                                    except:
                                        pass
                                        

                            else:
                                await ctx.send("You are already verified", ephemeral=True)
                    
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
                                rangee = random.randint(4,6)
                                result_str = ''.join(random.choice(letters) for i in range(rangee))
                                image = ImageCaptcha(width = 280, height = 90, fonts=["MangabeyRegular-rgqVO.ttf"], font_sizes=[80])
                                data = image.generate(result_str.lower())
                                image.write(result_str, f'{ctx.user.id}-captcha.jpg')
                                embed=nextcord.Embed(title=(f"Captcha"), description=(f"""You have 1 minute to answer the captcha correctly. 
                                                                                
The captcha will only be **undercase** **letters**.
If you get it wrong just click the verify button again and retry"""), colour=0xadd8e6)
                                try:
                                    await ctx.user.send(embed=embed, file=nextcord.File(f"{ctx.user.id}-captcha.jpg"))
                                    await ctx.send("Complete the captcha I have sent in our DMs to verify.")
                                    os.remove(f"{ctx.user.id}-captcha.jpg")
                                    def check(msg):
                                        return msg.author.id == ctx.user.id and msg.guild == None
                                    result_str = result_str.replace(" ", "")
                                    answer = await self.client.wait_for('message', check=check, timeout=120)
                                    if answer.content == result_str:
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
                                        try:
                                            await ctx.user.send(f"You have successfully verified in **{ctx.guild.name}**")
                                        except:
                                            await ctx.send(f"You have successfully verified", ephemeral=True)
                                        
                                        if not logchannel == None:
                                            try:
                                                await logchannel.send(embed=embed)
                                            except:
                                                pass
                                    else:
                                        try:
                                            await ctx.user.send(f"Incorrect answer, please try again. Correct answer was `{result_str}`")
                                        except:
                                            await ctx.send(f"Incorrect answer, please try again. Correct answer was `{result_str}`", ephemeral=True)
                                        
                                except asyncio.TimeoutError:
                                    try:
                                        await ctx.user.send("You ran out of time to answer the captcha, please try again.")
                                    except:
                                        await ctx.send("You ran out of time to answer the captcha, please try again.", ephemeral=True)

                                    

                                except Exception as e:
                                    print(e)
                                    await ctx.send("Couldn't DM you the captcha, make sure you have your DMs enabled for the server.", ephemeral=True)
                                    try:
                                        os.remove(f"{ctx.user.id}-captcha.jpg")
                                    except:
                                        pass
                            else:
                                await ctx.send("You are already verified", ephemeral=True)
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

    @nextcord.slash_command(name="verifymessage", description="Send the verification message to a channel", guild_ids=[801744339343507457])
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
            await ctx.response.defer()
            if custom:
                def check(message):
                    return message.author == ctx.user and message.channel == ctx.channel
                try:
                    titleq = await ctx.send("What do you want the title to be?")
                    title = await self.client.wait_for('message', check=check, timeout = 300)
                    descq = await title.reply("What do you want the description to be?")
                    desc = await self.client.wait_for("message", check=check, timeout=300)
                    if len(title.content) > 255:
                        await ctx.send("Your title must be less than 255 characters")
                    elif len(desc.content) > 3900:
                        await ctx.send("Your description must be less than 3900 characters")
                    elif len(title.content) + len(desc.content) > 4000:
                        await ctx.send("You description and title must be below 4000 characters")
                    else:
                        embed=nextcord.Embed(title=f"{title.content}", description=f"{desc.content}", colour=0xadd8e6)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long to answer. Please try again")
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
        if member.id in verifying:
            pass
        else:
            verifying.append(member.id)
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
                            kicked = True
                            index = verifying.index(member.id)
                            del verifying[index]

                    if kicked == False:
                        try:
                            unverifiedrole = None
                            if not data[2] == None:
                                unverifiedroleid = data[2]
                                unverifiedrole = member.guild.get_role(int(unverifiedroleid))
                                await member.add_roles(unverifiedrole)

                        except:
                            pass 

                        if data[6] == "enabled":
                            if data[4] == "0":
                                try:
                                    index = verifying.index(member.id)
                                    del verifying[index]
                                except:
                                    pass
                            
                            elif data[4] == "1":
                                try:
                                    index = verifying.index(member.id)
                                    del verifying[index]
                                except:
                                    pass

                            elif data[4] == "2":
                                try:
                                    veryroleid = data[1]
                                    veryrole = member.guild.get_role(int(veryroleid))
                                    unverifiedrole = None
                                    if not data[2] == None:
                                        unverifiedroleid = data[2]
                                        unverifiedrole = member.guild.get_role(int(unverifiedroleid))
                                    logchannel = None
                                    if not data[3] == None:
                                        logchannelid = data[3]
                                        logchannel = member.guild.get_channel(int(logchannelid))
                                    if (not veryrole in member.roles) or (unverifiedrole != None and unverifiedrole in member.roles):
                                        rangee = random.randint(4,6)
                                        result_str = ''.join(random.choice(letters) for i in range(rangee))
                                        image = ImageCaptcha(width = 280, height = 90, fonts=["MangabeyRegular-rgqVO.ttf"], font_sizes=[80])
                                        data = image.generate(result_str.lower())
                                        image.write(result_str, f'{member.id}-captcha.jpg')
                                        embed=nextcord.Embed(title=(f"Captcha"), description=(f"""You have 1 minute to answer the captcha correctly. 
                                                               
The captcha will only be **undercase** **letters**.
If you get it wrong just click the verify button again and retry"""), colour=0xadd8e6)
                                        try:
                                            await member.send(embed=embed, file=nextcord.File(f"{member.id}-captcha.jpg"))
                                            os.remove(f"{member.id}-captcha.jpg")
                                            def check(msg):
                                                return msg.author.id == member.id and msg.guild == None
                                            result_str = result_str.replace(" ", "")
                                            answer = await self.client.wait_for('message', check=check, timeout=120)
                                            if answer.content == result_str:
                                                embed =nextcord.Embed(title="Verification", description=f"{member.mention} has successfully verified", colour=0xadd8e6)
                                                try:
                                                    await member.add_roles(veryrole)
                                                    embed.add_field(name="Roles added", value=f"{veryrole.mention}")
                                                    if not unverifiedrole == None and unverifiedrole in member.roles:
                                                        try:
                                                            await member.remove_roles(unverifiedrole)
                                                            embed.add_field(name="Roles removed", value=f"{unverifiedrole.mention}")
                                                        except:
                                                            try:
                                                                await member.send("Failed to remove unverified role.")
                                                            except:
                                                                pass
                                                            embed.add_field(name="Roles removed", value=f"Failed to remove unverified role")
                                                            index = verifying.index(member.id)
                                                            del verifying[index]
                                                            if not logchannel == None:
                                                                try:
                                                                    await logchannel.send(embed=embed)
                                                                except:
                                                                    pass
                                                            return
                                                except Exception as e:
                                                    print(e)
                                                    try:
                                                        await member.send("Failed to add verified role")
                                                    except:
                                                        pass
                                                    embed.add_field(name="Roles added", value=f"Failed to give verified role")
                                                    index = verifying.index(member.id)
                                                    del verifying[index]
                                                    if not logchannel == None:
                                                        try:
                                                            await logchannel.send(embed=embed)
                                                        except:
                                                            pass
                                                    return
                                                try:
                                                    await member.send(f"You have successfully verified in **{member.guild.name}**")
                                                except:
                                                    pass
                                                
                                                if not logchannel == None:
                                                    try:
                                                        await logchannel.send(embed=embed)
                                                    except:
                                                        pass
                                            else:
                                                try:
                                                    await member.send(f"Incorrect answer, please try again. Correct answer was `{result_str}`")
                                                except:
                                                    pass
                                                
                                        except asyncio.TimeoutError:
                                            try:
                                                await member.send("You ran out of time to answer the captcha, please try again.")
                                            except:
                                                pass

                                            

                                        except Exception as e:
                                            print(e)
                                            try:
                                                os.remove(f"{member.id}-captcha.jpg")
                                            except:
                                                pass
                                    else:
                                        pass
                                
                                except Exception as e:
                                    print(e)

                            try:
                                index = verifying.index(member.id)
                                del verifying[index]
                            
                            except:
                                pass

            else:
                index = verifying.index(member.id)
                del verifying[index]



def setup(client):
    client.add_cog(VerifyMessage(client))
                    
