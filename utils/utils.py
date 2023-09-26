from .constants import COLOUR_BAD, COLOUR_GOOD, COLOUR_NEUTRAL, DBENDPOINT, DBNAME, DBPASS, DBUSER, PREMIUMLINK
import nextcord, math, random, pymysql
from string import ascii_letters, digits

def create_success_embed(title: str = "\u200b", description: str = "\u200b"):
    embed = nextcord.Embed(title=title, description=description, color=COLOUR_GOOD)
    embed.set_thumbnail(url="https://media.tenor.com/AWKzZ19awFYAAAAi/checkmark-transparent.gif")
    return embed

def create_warning_embed(title: str = "\u200b", description: str = "\u200b"):
    embed = nextcord.Embed(title=title, description=description, color=COLOUR_NEUTRAL)
    embed.set_thumbnail(url="https://c.tenor.com/26pNa498OS0AAAAi/warning-joypixels.gif")
    return embed

def create_error_embed(title: str = "\u200b", description: str = "\u200b"):
    embed = nextcord.Embed(title=title, description=description, color=COLOUR_BAD)
    embed.set_thumbnail(url="https://media.tenor.com/Gbp8h-dqDHkAAAAi/error.gif")
    return embed

def check_premium(self, guild: bool, user: bool, type_id: str) -> bool:
    conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
    cur = conn.cursor()
    if guild:
        cur.execute(f"SELECT * FROM sv_premium_guilds WHERE guild_id='{type_id}'")
        data = cur.fetchall()
        return True if data else False
    elif user:
        cur.execute(f"SELECT * FROM sv_premium_users WHERE user_id='{type_id}'")
        data = cur.fetchall()
        return True if data else False
    return None

def generate_dashboard(self, data):
    if data[0][6] == "no":
        autov = "Disabled"
    else:
        autov = "Enabled"
    return nextcord.Embed(title=f"Verification Dashboard", description=f"""Verified Role(s): {(",".join([('<@&' + i + '> ') for i in data[0][1].split(",")])) if data[0][1] else 'Not Set'}\nUnverified Role(s): {(",".join([('<@&' + i + '> ') for i in data[0][2].split(",")])) if data[0][2] else 'Not Set'} \nLog Channel: <#{data[0][3] if data[0][3] else 'Not Set'}> \nAuto Kick: {f"{data[0][5]} day(s)" if data[0][5] else 'Not Set'} \nAuto Verification ([Premium]({PREMIUMLINK}) Only): {autov}\nMinimum Captcha Length ([Premium]({PREMIUMLINK}) Only): {data[0][7]}\nMaximum Captcha Length ([Premium]({PREMIUMLINK}) Only): {data[0][8]}""")

def generate_random_string(min_length: int = 4, max_length: int = 5):
    return ''.join([random.choice(ascii_letters+digits) for i in range(min_length, max_length)])

def get_user_name(user) -> str:
    if not str(user.discriminator) == "0":
        return user
    return str(user.name)