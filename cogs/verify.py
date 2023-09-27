import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
from utils import check_premium, DBENDPOINT, DBNAME, DBPASS, DBUSER, generate_dashboard, create_warning_embed, COLOUR_MAIN, create_success_embed, create_error_embed
from views import DashboardButtons, VerifyButton, EmbedCreator
import pymysql

class Verify(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name=f"verifymessage", description=f"Send a verification message to a channel")
    async def verifymessage(self,
        interaction: Interaction,
        channel: GuildChannel = SlashOption(
            name=f"channel",
            description=f"The channel you want to send the verification message to",
            channel_types=[nextcord.ChannelType.text, nextcord.ChannelType.news],
            required=True
        ),
        customembed: str = SlashOption(
            name=f"custom-embed",
            description=f"Do you want to customise the embed sent to the verification channel?",
            choices={"Yes, I want to customise the embed": "True", "No, I don't want to customise the embed":"False"},
            required=False
        )):
        if not interaction.user.guild_permissions.administrator:
            await interaction.send(embed=create_warning_embed(title="Insufficient permissions", description="You need the `administrator` permission to use this."))
            return
        
        conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM guild_configs WHERE id='{interaction.guild.id}'")
        data = cur.fetchall()
        if not data:
            cur.execute(f"INSERT INTO guild_configs (id) VALUES ('{interaction.guild.id}')")
            conn.commit()

        if (not data[1]) and (not data[2]): # Checks to see if verified roles are set.
            await interaction.send(embed=create_error_embed(title="Incorrect Config!", description=f"You have no verified/unverified roles set, please use the `/dashboard` command to set them.")) # todo: Mention command.
            conn.commit()
            return

        embed=nextcord.Embed(title=f"Verification", description=f"To verify in the server press the button below and follow the instructions from there.", colour=COLOUR_MAIN)

        if customembed == "True":
            options = EmbedCreator()
            await interaction.response.send_modal(modal=options)
            await options.wait()
            embed=nextcord.Embed(title=options.embedtitle, description=options.embdeddesc, colour=COLOUR_MAIN)
        
        try:
            await channel.send(embed=embed, view=VerifyButton(self.client))
            await interaction.send(embed=create_success_embed(title=f"Message sent!", description=f"I have sent your verification message to {channel.mention}"))
        except:
            interaction.send(embed=create_error_embed(title=f"Error sending verification message!", description=f"I was unable to send the verification message to {channel.mention}. Ensure I have permission to `send_messages` and `embed_links` in {channel.mention}"))

        

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.client.add_view(VerifyButton(self.client))
            print("Loaded VerifyButton view")
        except Exception as e:
            print(e)
            print("Failed to load VerifyButton view")


def setup(client):
    client.add_cog(Verify(client))