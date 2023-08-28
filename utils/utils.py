from .constants import COLOUR_BAD, COLOUR_GOOD, COLOUR_NEUTRAL, DBENDPOINT, DBNAME, DBPASS, DBUSER
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

def check_premium(self, guild: bool, user: bool, type_id: str):
    conn = pymysql.connect(host=DBENDPOINT, port=3306, user=DBUSER, password=DBPASS, db=DBNAME)
    cur = conn.cursor()
    if guild:
        cur.execute(f"SELECT * FROM sv_premium_guilds WHERE id='{type_id}'")
        data = cur.fetchall()
        return True if data else False
    elif user:
        cur.execute(f"SELECT * FROM sv_premium_users WHERE id='{type_id}'")
        data = cur.fetchall()
        return True if data else False
    return None
        

def totalxp_to_level(total_xp):
    level = (-1 + math.sqrt(1 + 4*(total_xp // 50))) // 2
    threshold = (level+1)*100
    xp=total_xp - 50*(level**2 + level)
    return round(level), round(threshold), round(xp)

def level_to_totalxp(level):
    return 100*(level*(level+1))/2

def generate_random_string(length: int = 0):
    return ''.join([random.choice(ascii_letters+digits) for i in range(length if length else random.randint(5, 10))])

def get_user_name(user):
    if not str(user.discriminator) == "0":
        return user
    return str(user.name)