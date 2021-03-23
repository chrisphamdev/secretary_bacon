''' This bot was developed by Chris Pham
'''
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


from test import *

token = 'NzYwMDAyNTY3ODc4MzQ0NzE1.X3FtjA.xH_Yv5vWtMS-N8cBxk_Idl1zWHU'
client = commands.Bot(command_prefix=';')

nums = '1\N{variation selector-16}\N{combining enclosing keycap}'


# process the custom database

# each member will be store in the data base under the
# form 'userid balance' seperated by a space
with open('currencydb.txt', 'r') as file:
    database_raw = file.read().split('\n')
    database = {}
    for user in database:
        

# Custom help message - to be done
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("Đéo có help command đâu.")


@client.event
async def on_member_join(member):
    general_channel = client.get_channel(624197530816610307)
    await general_channel.send(f'Chào mừng {member.display_name} tới với công ty TNHH FUHO.')
@client.event
async def on_member_remove(member):
    general_channel = client.get_channel(624197530816610307)
    await general_channel.send(f'{member.display_name} đã từ chức khỏi FUHO.')

@client.event
async def on_ready():
    print('Thư ký Bacon has been deployed.')

@client.command()
async def info(ctx):
    await ctx.send('`This bot was developed by Chris Pham.\nAny feedback will be kindly appreciated to Chris P Bacon#0047.`')


@client.command()
async def beg(ctx):
    await ctx.send('Any donation would be kindly appreciated in League\'s RP to the account Chris P Bacon#OCE :   ^)')

  
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Delay giữa client với server là {round(client.latency * 1000)}ms.')


@client.command()
async def tao_role(ctx):
    text = '\n1. League\n2. Minecraft\n3. Among Us\n4. CS:GO'
    embedVar=discord.Embed(title="React message này để lấy role.", description=text, color=0x14cad7)
    embedVar.set_image(url='https://cdn1.dotesports.com/wp-content/uploads/2020/07/07104742/Spirit_Blossom_Yasuo.jpg')
    await ctx.send(embed=embedVar)

@client.command()
async def react_role(ctx, messageID, index):
    msg = await ctx.fetch_message(messageID)
    for num in range(1, index+1):
        emj = str(num)+'\N{variation selector-16}\N{combining enclosing keycap}'
        await msg.add_reaction(emj)


@client.command()
async def create_colour(ctx):
    text = '\n1. Hồng bóng gồng\n2. Tím như bím\n3. Vàng dễ dàng\n4. Trắng thượng đẳng\n5. Đen đéo có vần vì đen bị cảnh sát đè chết'
    embedVar=discord.Embed(title="React message này để lấy màu.", description=text, color=0xdeda10)
    embedVar.set_image(url='https://i.pinimg.com/originals/f1/75/68/f17568e542beda0b2b5e11acbdb07288.jpg')
    await ctx.send(embed=embedVar)


@client.event
async def on_raw_reaction_add(data):
    if data.message_id == 760045988038574090:
        member = client.get_user(data.user_id)
        if data.emoji.name == '1️⃣':
            role = get(data.member.guild.roles, id=760046394370818088)
            await data.member.add_roles(role)
        if data.emoji.name == '2️⃣':
            role = get(data.member.guild.roles, id=760046446350696488)
            await data.member.add_roles(role)
        if data.emoji.name == '3️⃣':
            role = get(data.member.guild.roles, id=760046479929770014)
            await data.member.add_roles(role)
        if data.emoji.name == '4️⃣':
            role = get(data.member.guild.roles, id=760046544640147456)
            await data.member.add_roles(role)
    
    if data.message_id == 760112391286685756:
        member = client.get_user(data.user_id)
        if data.emoji.name == '1️⃣':
            role = get(data.member.guild.roles, id=760110053314920479)
            await data.member.add_roles(role)
        if data.emoji.name == '2️⃣':
            role = get(data.member.guild.roles, id=760110224592994304)
            await data.member.add_roles(role)
        if data.emoji.name == '3️⃣':
            role = get(data.member.guild.roles, id=760110422384050178)
            await data.member.add_roles(role)
        if data.emoji.name == '4️⃣':
            role = get(data.member.guild.roles, id=760110601685958656)
            await data.member.add_roles(role)
        if data.emoji.name == '5️⃣':
            role = get(data.member.guild.roles, id=760110699992055869)
            await data.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(data):
    if data.message_id == 760112391286685756:
        member = client.get_user(data.user_id)
        guild1 = client.get_guild(data.guild_id)
        for mem in guild1.members:
            if mem.id == member.id:
                reacted_member = mem
                break
        if data.emoji.name == '1️⃣':
            role = get(guild1.roles, id=760110053314920479)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '2️⃣':
            role = get(guild1.roles, id=760110224592994304)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '3️⃣':
            role = get(guild1.roles, id=760110422384050178)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '4️⃣':
            role = get(guild1.roles, id=760110601685958656)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '5️⃣':
            role = get(guild1.guild.roles, id=760110699992055869)
            await reacted_member.remove_roles(role)
    
    if data.message_id == 760045988038574090:
        member = client.get_user(data.user_id)
        guild1 = client.get_guild(data.guild_id)
        for mem in guild1.members:
            if mem.id == member.id:
                reacted_member = mem
                break
        if data.emoji.name == '1️⃣':
            role = get(guild1.roles, id=760046394370818088)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '2️⃣':
            role = get(guild1.roles, id=760046446350696488)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '3️⃣':
            role = get(guild1.roles, id=760046479929770014)
            await reacted_member.remove_roles(role)
        if data.emoji.name == '4️⃣':
            role = get(guild1.roles, id=760046544640147456)
            await reacted_member.remove_roles(role)

@client.command()
async def quyetdinh(ctx, option1, option2):
    opt = random.randrange(1,3)
    if opt == 1:
        await ctx.send(option1)
    else:
        await ctx.send(option2)

@client.command()
async def dis(ctx, user):
    disrap = [f'Địt mẹ thằng {user}', f'{user}\'s mum is gay', f'{user}\'s mama is so fat she walked past the TV and I missed 3 episodes.', f'{user} ngu tới mức solo Yasuo thua Triều.']
    option = random.randrange(0, len(disrap))
    await ctx.send(disrap[option])
  
@client.command()
async def say(ctx, *, words):
    await ctx.send(words)

@client.command()
async def rank_solo(ctx, *, username):
    profile = get_profile(username)
    
    embed=discord.Embed(title="Solo rank query ", color=0x0db1e7)
    embed.add_field(name="summoner_name", value="values", inline=False)
    embed.set_footer(text="Powered by Chris P Bacon")
    await ctx.send(embed=embed)

@client.command()
async def claim(ctx, amount):
    pass


client.run(token)
