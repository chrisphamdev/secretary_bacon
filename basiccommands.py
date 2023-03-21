# This module contains all basic commands and functionality of the bot

import discord
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random
from carlookup import *
from gpt import *

from main import bot

# Custom help message - to be done
bot.remove_command('help')
@bot.command()
async def help(ctx):
    await ctx.send("Đéo có help command đâu.")

@bot.event
async def on_command_error(ctx, error):
    if type(error) == discord.ext.commands.errors.CommandOnCooldown:
        await ctx.send('Có làm thì mới có ăn. Chỉ nhận được lương 1 lần trong 5 phút.')

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
    await ctx.send(f'Pong! Delay giữa client với server là {round(bot.latency * 1000)}ms.')

@bot.command()
async def quyetdinh(ctx, option1, option2):
    opt = random.randrange(1,3)
    if opt == 1:
        await ctx.send(option1)
    else:
        await ctx.send(option2)

@bot.command()
async def dis(ctx, user):
    disrap = [f'Địt mẹ {user}', f'{user} rác tới mức solo thua Benny', 
        f'Người ta đội mũ bảo hiểm để bảo vệ não, nhưng riêng {user} không cần đội mũ bảo hiểm.',
        f'{user} rác hơn cả Ornn của Bách',
        f'Chó cứ sủa, người cứ đi. Người đi rồi {user} vẫn sủa.',
        f'{user} rác hơn cả Blitz của Trí',
        f'Nơi {user} thuộc về:', #https://images.news18.com/ibnlive/uploads/2021/08/windows.jpg
        f'Khi buồn, {user} hãy nhớ tới QTV', #https://memedaily.vn/storage/meme/co-thuc-luc-thua-moi-buon-khong-co-thuc-luc-ma-thua-thi-sao-phai-buon.jpg
        f'https://cdn.discordapp.com/attachments/948390765267128331/948390865221615636/274997853_162298952810574_3432804555341767487_n.jpg',
        f'{user} hơi non.',
        f'Tôi **XIN** {user} đấy.',
        f'https://cdn.discordapp.com/attachments/948390765267128331/948390880866353202/275133068_162298869477249_3695419714806402304_n.jpg'
        ] 
        
    option = random.randrange(0, len(disrap))
    await ctx.send(disrap[option])
    if option == 6:
        await ctx.send('https://images.news18.com/ibnlive/uploads/2021/08/windows.jpg')
    if option == 7:
        await ctx.send('https://memedaily.vn/storage/meme/co-thuc-luc-thua-moi-buon-khong-co-thuc-luc-ma-thua-thi-sao-phai-buon.jpg')
        
  
@bot.command()
async def say(ctx, *, words):
    await ctx.send(words)

@bot.command()
async def spam(ctx, *, message):
    num_of_times = random.randrange(4,10)
    for i in range(num_of_times):
        await ctx.send(message)

@bot.command()
async def status(ctx, *, game_name):
    await bot.change_presence(activity=discord.Game(name=game_name))

@bot.command()
async def lotto(ctx):
    output = ''
    for i in range(6):
        output += str(random.randrange(1,41))
        output += ' '
    await ctx.send(output)

@bot.command()
async def plate(ctx, *, plate):
    year, make, model, color, submodel, car_type, cc_rating, photo_url, page_url = plate_lookup(plate)

    embed=discord.Embed(title=plate.upper(), url=page_url, color=0x00ffd5)
    if not 'upload-your-photo' in photo_url:
        embed.set_thumbnail(url=photo_url)
    embed.add_field(name=f'{year} {make} {model} {submodel}', value='', inline=False)
    embed.add_field(name="Color", value=f'{color}', inline=True)
    embed.add_field(name="CC Rating", value=f'{cc_rating}cc', inline=True)
    if car_type != '':
        embed.add_field(name="Type", value=f'{car_type}', inline=False)
    embed.set_footer(text="Data fetched from carjam.co.nz")

    await ctx.send(embed=embed)

@bot.command()
async def gpt(ctx, *, prompt):
    response = generate_response(prompt)
    await ctx.send(response)

@bot.command()
async def clown(ctx, *, prompt):
    response = generate_sarcastic_response(prompt)
    await ctx.send(response)

    