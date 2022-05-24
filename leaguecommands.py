'''
# This module contain the league profile lookup functionality of the bot

import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random

from helper.opgglookup import *
from main import bot

profile = get_profile('Chrispy Bacon')
    
print(get_solo_rank(profile))
@bot.command()
async def rank_solo(ctx, *, username):
    profile = get_profile(username)
    
    summoners_icon, rank_solo, win, loss, winrate = get_solo_rank(profile)

    ranked_solo_line = '\n\n\nRanked Solo: {0:<10}\n\n'.format(rank_solo)
    win_loss_line = '\n\n\nWin - Loss: {}W {}L\n\n'.format(win, loss)
    winrate_line = 'Winrate: {0:>20}%\n\n'.format(winrate)

    comment = '\n\n'
    if winrate < 46:
        comment = 'Winrate thấp, rác vcl.'
    if winrate >= 46 and winrate < 49:
        comment = 'Dưới trung bình, còn cần cố gắng.'
    if winrate >=49 and winrate < 52:
        comment = 'Winrate trung bình, không có gì đặc sắc.'
    if winrate >= 52 and winrate < 55:
        comment = 'Winrate khá cao, respect.'
    if winrate >= 55:
        comment = 'Winrate cao, chắc chắn hack, report Riot pls.'

    if win+loss >= 500:
        comment += '. Chơi nhiều vloz, get a life.'
    
    
    embed=discord.Embed(title=username, color=0x07edea)
    embed.set_thumbnail(url="https:"+summoners_icon)
    embed.add_field(name=ranked_solo_line, value=win_loss_line+winrate_line+comment, inline=True)
    embed.set_footer(text="Powered by Chris P Bacon")
    await ctx.send(embed=embed)
'''