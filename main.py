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
import traceback
from discord.utils import get
import time
from tinydb import TinyDB, Query

bot = commands.Bot(command_prefix='.')

# Import the implemented functionalities from different modules
from basiccommands import *
from archive import *
from pokergame import *
from worldcup import *

@bot.command()
async def testing(ctx):
    userername = bot.get_user(ctx.author.id).name
    await ctx.send(userername)


@bot.event
async def on_command_error(ctx, error):
    # Without this, command exceptions only print to the console (or are
    # swallowed entirely), so a failing command just leaves the bot
    # "typing..." with nothing sent and no visible error.
    if isinstance(error, commands.CommandNotFound):
        return
    traceback.print_exception(type(error), error, error.__traceback__)
    await ctx.send(f'⚠️ Command failed: `{error}`')


