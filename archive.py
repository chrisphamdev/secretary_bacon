# This module is the archive of all functions that was used to create
# the react role functionality of the bot, and is being run on the
# background to check for any future reaction

import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random
from discord.utils import get
import time

from main import bot
nums = '1\N{variation selector-16}\N{combining enclosing keycap}'

@bot.command()
async def tao_role(ctx):
    text = '\n1. League\n2. Minecraft\n3. Among Us\n4. CS:GO'
    embedVar=discord.Embed(title="React message này để lấy role.", description=text, color=0x14cad7)
    embedVar.set_image(url='https://cdn1.dotesports.com/wp-content/uploads/2020/07/07104742/Spirit_Blossom_Yasuo.jpg')
    await ctx.send(embed=embedVar)

@bot.command()
async def react_role(ctx, messageID, index):
    msg = await ctx.fetch_message(messageID)
    for num in range(1, index+1):
        emj = str(num)+'\N{variation selector-16}\N{combining enclosing keycap}'
        await msg.add_reaction(emj)


@bot.command()
async def create_colour(ctx):
    text = '\n1. Hồng bóng gồng\n2. Tím như bím\n3. Vàng dễ dàng\n4. Trắng thượng đẳng\n5. Đen đéo có vần vì đen bị cảnh sát đè chết'
    embedVar=discord.Embed(title="React message này để lấy màu.", description=text, color=0xdeda10)
    embedVar.set_image(url='https://i.pinimg.com/originals/f1/75/68/f17568e542beda0b2b5e11acbdb07288.jpg')
    await ctx.send(embed=embedVar)


@bot.event
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

@bot.event
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
