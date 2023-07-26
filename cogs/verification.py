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
                    
