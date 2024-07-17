import os
import discord
import discord.ui
import aiohttp
from discord.ext import commands

# Misc
from keep_alive import keep_alive
from dotenv import load_dotenv
keep_alive()
load_dotenv()

# Folders / Files
from Bot_Commands.Role import *
from Bot_Commands.Riot import *
from Bot_Commands.General import *

# Roles, User ID's
Admin = os.getenv("Admin")
Aram = os.getenv("Aram")
Discord = os.getenv("Discord")
Riot_API = os.getenv("Riot_API")

# Bot Intents
intents = discord.Intents().all()
intents.messages = True
intents.reactions = True
intents.message_content = True

# Bot Misc
activity = discord.Activity(type=discord.ActivityType.watching, name="you rn.")
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all(), status = discord.Status.do_not_disturb, activity=activity)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(Discord)