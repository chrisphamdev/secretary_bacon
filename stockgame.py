import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random


from database.databasehandler import *
from stocksimulator.stocklookup import get_info
from main import bot


# decode the holdings from the database
def decode_holdings(userid):
    user_db_obj = dict(db.search(database.id == userid)[0])
    if user_db_obj['holdings'] == '':
        return {}
    holdings = user_db_obj['holdings'][:-1].split(';')
    holdings_dict = {}

    for i in range(len(holdings)):
        holdings_dict[holdings[i].split()[0]] = float(holdings[i].split()[1])

    return holdings_dict

def encode_holdings(holdings_dict):
    output = ''
    for item in holdings_dict:
        output += '{} {};'.format(item, holdings_dict[item])
    return output

# calculate the total value of a person portfolio
def calculate_capital(userid):
    user_db_obj = dict(db.search(database.id == userid)[0])
    holdings = decode_holdings(userid)

    capital = user_db_obj['wallet']

    if len(holdings) == 0:
        return capital

    for symbol in holdings:
        stock = get_info(symbol)
        capital += stock.current_price*holdings[symbol]
    return capital


@bot.command()
async def query(ctx, symbol):
    stock_object = get_info(symbol)
    if stock_object.current_change >= 0:
        emb_color = 0x05d61e
    else:
        emb_color = 0xf20707

    values = ''
    values += 'Current price :  {}\n'.format(stock_object.current_price)
    values += 'Current change:  {}\n'.format(stock_object.current_change)
    values += 'Change in %   :  {}\n'.format(stock_object.current_change_percent)
    embed=discord.Embed(title="{} lookup".format(stock_object.symbol), color=emb_color)
    embed.add_field(name=stock_object.company_name, value=values, inline=False)
    embed.set_footer(text="Retrieved from www.marketwatch.com")
    await ctx.send(embed=embed)

@bot.command()
async def stock_init(ctx):
    userid = ctx.author.id
    
    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'wallet':100000, 'holdings':''})
        await ctx.send('Profile created.')
    else:
        await ctx.send('Profile existed.')
    
@bot.command()
async def balance(ctx):
    holdings = decode_holdings(ctx.author.id)
    capital = calculate_capital(ctx.author.id)
    output = '```json\nPORTFOLIO SUMMARY\n\n'
    output += '{:<20}| {:<10} | {:<10} | {:<10}\n'.format('    Company name', '  Symbol', 'Share owned', 'Current value')
    seperator = '-'*62
    output += seperator + '\n'
    for symbol in holdings:
        target_stock = get_info(symbol)
        line = '{:<20}| {:<10} | {:<10.2f}  | {:<10.2f}\n'.format(target_stock.company_name, target_stock.symbol, holdings[symbol], target_stock.current_price*holdings[symbol])
        output += line
    output += seperator + '\n\n'
    output += 'CAPITAL: ${:.2f}'.format(calculate_capital(ctx.author.id))
    output += '```'
    await ctx.send(output)
    
@bot.command()
async def buy(ctx, symbol, amount):
    user_db_obj = dict(db.search(database.id == ctx.author.id)[0])
    amount_bought = round(float(amount),2)
    service_fee = amount_bought*0.005

    if amount_bought > user_db_obj['wallet']:
        await ctx.send('Không có tiền mà còn đua đòi?')
    if amount_bought <= 0:
        await ctx.send('Invalid argument')
    else:
        target_stock = get_info(symbol)

        share_owned = round(amount_bought/target_stock.current_price,2)
        new_balance = user_db_obj['wallet'] - amount_bought - service_fee
        holdings = decode_holdings(ctx.author.id)

        # check if user already owned this symbol
        if symbol.upper() not in holdings:
            holdings[symbol.upper()] = share_owned
        else:
            holdings[symbol.upper()] += share_owned

        updated_holdings = encode_holdings(holdings)
        db.update({'wallet':new_balance}, database.id == ctx.author.id)
        db.update({'holdings':updated_holdings}, database.id == ctx.author.id)

        await ctx.send('Đã mua {:.2f} share của công ty {}. Còn lại ${:.2f} tiền mặt.'.format(share_owned, target_stock.company_name, new_balance))

@bot.command()
async def sell(ctx, symbol, amount):
    user_db_obj = dict(db.search(database.id == ctx.author.id)[0])
    amount_selling = round(float(amount), 2)

    holdings = decode_holdings(ctx.author.id)

    if symbol.upper() not in holdings:
        await ctx.send('Làm đéo gì có mà bán?')
    else:
        target_stock = get_info(symbol)
        owned_amount = target_stock.current_price * holdings[symbol.upper()]
        if amount_selling > owned_amount:
            await ctx.send('Làm đéo gì có mà bán?')
        else:
            remaining_amount = owned_amount - amount_selling
            holdings[symbol.upper()] = remaining_amount/target_stock.current_price
            updated_holdings = encode_holdings((holdings))
            db.update({'holdings':updated_holdings}, database.id == ctx.author.id)
            db.update({'wallet':user_db_obj['wallet']+amount_selling}, database.id == ctx.author.id)
            await ctx.send('Đã bán ${:.2f}, tương đương {:.2f} share {}. Còn lại ${:.2f} tiền mặt'.format(amount_selling, amount_selling/target_stock.current_price, target_stock.symbol, user_db_obj['wallet']+amount_selling))

@bot.command()
async def sellall(ctx, symbol):
    user_db_obj = dict(db.search(database.id == ctx.author.id)[0])

    holdings = decode_holdings(ctx.author.id)

    if symbol.upper() not in holdings:
        await ctx.send('Làm đéo gì có mà bán?')
    else:
        target_stock = get_info(symbol)
        amount_selling = holdings[symbol.upper()]*target_stock.current_price
        share_num = holdings[symbol.upper()]
        holdings.pop(symbol.upper())
        new_balance = user_db_obj + amount_selling
        await ctx.send('Đã bán ${:.2f}, tương đương {:.2f} share {}. Còn lại ${:.2f} tiền mặt'.format(amount_selling, share_num, target_stock.symbol, new_balance))
        updated_holdings = encode_holdings((holdings))
        db.update({'holdings':updated_holdings}, database.id == ctx.author.id)
        db.update({'wallet':new_balance}, database.id == ctx.author.id)

@bot.command()
async def cash(ctx):
    user_db_obj = dict(db.search(database.id == ctx.author.id)[0])
    await ctx.send('Còn lại ${:.2f} tiền mặt'.format(user_db_obj['wallet']))