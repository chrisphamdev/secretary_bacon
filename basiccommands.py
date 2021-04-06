# This module contains all basic commands and functionality of the bot

import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random

from main import bot

# Custom help message - to be done
bot.remove_command('help')
@bot.command()
async def help(ctx):
    await ctx.send("Đéo có help command đâu.")

@bot.event
async def on_command_error(ctx, error):
    if type(error) == discord.ext.commands.errors.CommandOnCooldown:
        await ctx.send('Có làm thì mới có ăn. Chỉ nhận được lương 1 lần trong 10 phút.')

@bot.event
async def on_member_join(member):
    general_channel = client.get_channel(624197530816610307)
    await general_channel.send(f'Chào mừng {member.display_name} tới với công ty TNHH FUHO.')
@bot.event
async def on_member_remove(member):
    general_channel = client.get_channel(624197530816610307)
    await general_channel.send(f'{member.display_name} đã từ chức khỏi FUHO.')

@bot.event
async def on_ready():
    print('Thư ký Bacon has been deployed.')

@bot.command()
async def info(ctx):
    await ctx.send('`This bot was developed by Chris Pham.\nAny feedback will be kindly appreciated to Chris P Bacon#0047.`')


@bot.command()
async def beg(ctx):
    await ctx.send('Any donation would be kindly appreciated in League\'s RP to the account Chris P Bacon#OCE :   ^)')

  
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Delay giữa client với server là {round(client.latency * 1000)}ms.')

@bot.command()
async def quyetdinh(ctx, option1, option2):
    opt = random.randrange(1,3)
    if opt == 1:
        await ctx.send(option1)
    else:
        await ctx.send(option2)

@bot.command()
async def dis(ctx, user):
    disrap = [f'Địt mẹ thằng {user}', f'{user}\'s mum is gay', f'{user}\'s mama is so fat she walked past the TV and I missed 3 episodes.', f'{user} ngu tới mức solo Yasuo thua Triều.']
    option = random.randrange(0, len(disrap))
    await ctx.send(disrap[option])
  
@bot.command()
async def say(ctx, *, words):
    await ctx.send(words)
