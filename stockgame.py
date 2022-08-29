import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random

from database.databasehandler import *
from stocksimulator.stocklookup import *
from main import bot
from  yahoo_fin import stock_info

@bot.command()
async def startTrade(ctx):
    msg = create_trading_profile(ctx.author.id)

    if msg == 'ID existed.':
        await ctx.send('Profile đã tồn tại, không cần khởi tạo.')
    else:
        await ctx.send('Profile đã được khởi tạo. Chúc bạn may mắn.')
    
@bot.command()
async def cash(ctx):
    summary = get_summary(ctx.author.id)
    if summary == 'User does not exist.':
        await ctx.send('Profile không tồn tại. Khởi tạo bằng command `startTrade`.')
    else:
        await ctx.send('Bạn có $' + str(summary[0]) + ' tiền mặt.')

@bot.command()
async def buy(ctx, symbol, amount):
    msg = buy_stock(ctx.author.id, symbol, int(amount))
    if msg == 'User does not exist.':
        await ctx.send('Profile không tồn tại. Khởi tạo bằng command `startTrade`.')
    elif msg == 'Insufficient balance.':
        await ctx.send('Không đủ tiền. Hơi non.')
    else:
        await ctx.send('Đã mua ' + str(msg) + ' share ' + symbol.upper() + '.')


@bot.command()
async def sell(ctx, symbol, amount):
    msg = sell_stock(ctx.author.id, symbol, int(amount))
    if msg == 'User does not exist.':
        await ctx.send('Profile không tồn tại. Khởi tạo bằng command `startTrade`.')
    elif msg == 'Insufficient amount.':
        await ctx.send('Không đủ chừng đó share để bán. Hơi non.')
    elif msg == 'You don\'t own any share of this company.':
        await ctx.send('Làm gì có mà bán? Xin đấy.')
    else:
        await ctx.send('Bán share thành công.')

@bot.command()
async def sellall(ctx, symbol):
    msg = sell_all_stock(ctx.author.id, symbol)
    if msg == 'User does not exist.':
        await ctx.send('Profile không tồn tại. Khởi tạo bằng command `startTrade`.')
    elif msg == 'You don\'t own any share of this company.':
        await ctx.send('Làm gì có mà bán. Xin đấy.')
    else:
        await ctx.send('Bán share thành công.')

@bot.command()
async def summary(ctx):
    summary = get_summary(ctx.author.id)
    user_balance = float(summary[0])
    holdings = summary[1]
    capital = user_balance

    output = '```json\nPORTFOLIO SUMMARY\n\n'
    output += '{:<20}| {:<10} | {:<10} | {:<10}\n'.format('    Company name', '  Symbol', 'Share owned', 'Current value')
    output += '-'*62 + '\n'
    for symbol in holdings:
        company_name = yf.Ticker(symbol.upper()).info['longName']
        if len(company_name) >= 15:
            company_name = company_name[:12]
        
        current_price = stock_info.get_live_price(symbol)
        current_value = current_price*holdings[symbol]
        capital += current_value
        line = '{:<20}| {:<10} | {:<10.2f}  | {:<10.2f}\n'.format(company_name, symbol.upper(), holdings[symbol], current_value)
        output += line
    
    output += '-'*62 + '\n\n'
    output += 'WALLET       : ${:.2f}\n'.format(user_balance)
    output += 'CAPITAL      : ${:.2f}\n'.format(capital, 2)
    output += 'TOTAL GAIN   : {}%'.format(round((capital/100000 - 1)*100))
    output += '```'
    await ctx.send(output)


@bot.command()
async def get_db_as_string(ctx):
    db_as_string = str(get_holdings_db())
    await ctx.send(str(get_holdings_db()))

@bot.command()
async def rewrite_db(ctx, *, new_db):
    output = rewrite_db_from_str(new_db)
    await ctx.send(output)
