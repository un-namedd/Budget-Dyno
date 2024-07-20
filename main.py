import os
import discord
import discord.ui
import time
import platform
from discord.ext import commands
from colorama import Back, Fore, Style
import aiohttp

from dynocmds.riotapi import rito # type: ignore
from dynocmds.generaluse import generalcmds # type: ignore
from dynocmds.rolecmds import rolecmds # type: ignore

Riot_API = os.getenv('Riot_API')
Aram = os.getenv('Aram_ID')
Admin = os.getenv('Admin_ID')
Owner = os.getenv('Owner')

class Client(commands.Bot):
    
    def __init__(self):
        super().__init__(command_prefix="!", intents = discord.Intents().all(), status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="you rn."))
        
        self.cogslist = ["dynocmds.riotapi", "dynocmds.generaluse", "dynocmds.rolecmds"]
        
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
            
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")


client = Client()

client.run(os.environ['Discord_Token'])
