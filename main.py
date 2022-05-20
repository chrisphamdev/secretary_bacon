# This bot was developed by Chris Pham 
# This bot was created to manage the server Cong ty TNHH MTV Fuho
# All enquiries please contact chrisphamdev@gmail.com
# All use of this bot must be approved by Chris Pham(TM)


import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import logging
import random
from discord.utils import get
import time
from tinydb import TinyDB, Query

bot = commands.Bot(command_prefix='.')

# Import the implemented functionalities from different modules
from basiccommands import *
from archive import *
from leaguecommands import *
from casino import *
from stockgame import *

@bot.command()
async def testing(ctx):
    userername = bot.get_user(ctx.author.id).name
    await ctx.send(userername)


