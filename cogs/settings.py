import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import pymysql, json



class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open('dbconfig.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]