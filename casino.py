# This module contain the gambling functionality of the bot

import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import asyncio
import time
from discord import client
import random


from database.databasehandler import *
from main import bot

@bot.command()
@commands.cooldown(1, 600)
async def claim(ctx):
    userid = ctx.author.id

    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'balance':0})
    
    # look for the user object
    user_db_obj = db.search(database.id == userid)[0]
    # extract the balance from the user object
    user_balance = float(str(user_db_obj).split()[-1][:-1])
    
    # update with the new balance
    claimed_value = random.randrange(100, 300)
    user_balance += claimed_value
    db.update({'balance':user_balance}, database.id == userid)

    embed=discord.Embed(title='', color=0x07edea)
    embed.add_field(name='Tới tháng lãnh lương', value='\n\nNhận lương thành công. ${} đã được thêm vào tài khoản.'.format(claimed_value), inline=False)
    embed.set_footer(text="Số dư hiện tại: ${}".format(user_balance))
    await ctx.send(embed=embed)


@bot.command()
async def gamble(ctx, amount=100):
    userid = ctx.author.id

    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'balance':0})
        await ctx.send('Ở cái xã hội này phải chịu khó làm, chịu khó học hỏi, khắc có tiền. Nay không kiếm được nhiều thì kiếm được ít, mình tích tiểu thành đại, mình chưa có thì mình không được chơi bời. Mình chưa có thì mình đừng có ăn chơi lêu lổng, đừng có a dua a tòng, đàn đúm.\n     -anh Huấn - 2020.')
    
    # look for the user object
    user_db_obj = db.search(database.id == userid)[0]
    # extract the balance from the user object
    user_balance = float(str(user_db_obj).split()[-1][:-1])

    if user_balance == 0 or amount>user_balance or amount <= 0:
        message = 'Không có tiền mà đòi đánh bạc? Người không chơi là ngưòi thắng.'
    
    else:
        choices = [0, 0, 0, 0, 1.5, 1.5, 1.5, 2, 2, 3]
        multiplier = choices[random.randrange(0, len(choices))]

        user_balance = user_balance - amount
        db.update({'balance':user_balance}, database.id == userid)
        amount = amount*multiplier
        user_balance += amount
        db.update({'balance':user_balance}, database.id == userid)
        
        if multiplier == 0:
            message = 'Chúc mừng, bạn đã mất hết tiền. Người không chơi là người thắng.'
        if multiplier > 0:
            message = 'Đánh bạc thành công, bạn đã x{} số tiền bỏ ra (${}).'.format(multiplier, amount/multiplier)

    embed=discord.Embed(title='', color=0x07edea)
    embed.add_field(name='FEELING LUCKY KID?', value=message, inline=False)
    embed.set_footer(text="Số dư hiện tại: ${}".format(user_balance))
    await ctx.send(embed=embed)

@bot.command()
async def balance(ctx):
    userid = ctx.author.id

    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'balance':0})

    # look for the user object
    user_db_obj = db.search(database.id == userid)[0]
    # extract the balance from the user object
    user_balance = float(str(user_db_obj).split()[-1][:-1])

    await ctx.send('Số dư trong tài khoản của bạn là ${}.'.format(user_balance))  

@bot.command()
async def steal(ctx, mentioned_user):
    member, mentioned_user = ctx.author, ctx.message.mentions[0]

    steal_success = random.choice([False, False, False, True, True])

    if len(db.search(database.id == mentioned_user.id)) == 0:
        db.insert({'id':mentioned_user.id, 'balance':0})
    
    # look for the user object
    author_obj = db.search(database.id == member.id)[0]
    # extract the balance from the user object
    author_balance = float(str(author_obj).split()[-1][:-1])

    # look for the user object
    victim_obj = db.search(database.id == mentioned_user.id)[0]
    # extract the balance from the user object
    victim_balance = float(str(victim_obj).split()[-1][:-1])

    if victim_balance <= 100:
        message = 'Đừng cướp của người nghèo thằng lồn vô tâm.'
        await ctx.send(message)
    elif author_balance <= 50:
        message = 'Không có tiền mà đòi đi ăn cướp?'
        await ctx.send(message)
        return
    elif steal_success:
        author_balance += 50
        victim_balance -= 50
        db.update({'balance':author_balance}, database.id == member.id)
        db.update({'balance':victim_balance}, database.id == mentioned_user.id)
        message = 'Cướp thành công từ {}, số dư mới là `${}`'.format(mentioned_user.mention, author_balance)
        await ctx.send(message)
    elif not steal_success:
        author_balance -= 50
        db.update({'balance':author_balance}, database.id == member.id)
        message = 'Không làm mà đòi có ăn?\nTrộm cắp bị cảnh sát bắt, phạt $50.\nSố dư mới ${}.'.format(author_balance)
        await ctx.send(message)

@bot.command()
async def leaderboard(ctx):
    leaderboard = []

    for user in db:
        userid = int(str(user).split()[1][:-1])
        username = None
        user_balance = float(str(user).split()[-1][:-1])
    
        if userid == 342576375523311616:
            username = 'Quân'
        if userid == 417125704807874570:
            username = 'Bách'
        if userid == 355905526745268226:
            username = 'Minh'
        if userid == 760002567878344715:
            username = 'Thư ký Bacon'
        if userid == 385348785733107714:
            username = 'Đức Anh'
        if userid == 234196333202767874:
            username = 'Đức'
        if userid == 455655526156599306:
            username = 'Trí'
        if username is None:
            username = str(userid)
        
        leaderboard += [(user_balance, username)]
 
    leaderboard.sort()
    leaderboard.reverse()

    message = '```json\n'
    for elm in leaderboard:
        message += '{:<30}|  {}'.format(elm[1], elm[0])
        message += '\n'
    message = message[:-1]
    message += '```'


    await ctx.send(message)

@bot.command()
async def give(ctx, mentioned_user, amount):
    member, mentioned_user = ctx.author, ctx.message.mentions[0]
    amount = float(amount)

    if len(db.search(database.id == mentioned_user.id)) == 0:
        db.insert({'id':mentioned_user.id, 'balance':0})
    if len(db.search(database.id == member.id)) == 0:
        db.insert({'id':member.id, 'balance':0})
    
    # look for the user object
    author_obj = db.search(database.id == member.id)[0]
    # extract the balance from the user object
    author_balance = float(str(author_obj).split()[-1][:-1])

    # look for the user object
    victim_obj = db.search(database.id == mentioned_user.id)[0]
    # extract the balance from the user object
    victim_balance = float(str(victim_obj).split()[-1][:-1])

    if amount > author_balance:
        await ctx.send('Không có tiền bày đặt bố thí?')
    elif member.id == mentioned_user.id:
        await ctx.send('Invalid arguments.')
    elif amount <= 0:
        await ctx.send('Invalid arguments.')
    else:
        if member.id != mentioned_user.id:
            author_balance -= amount
            victim_balance += amount
            db.update({'balance':author_balance}, database.id == member.id)
            db.update({'balance':victim_balance}, database.id == mentioned_user.id)
            await ctx.send('{} donated `${}` cho {}'.format(member.mention, amount, mentioned_user.mention))

@bot.command()
@commands.has_permissions(administrator=True)
async def reset_database(ctx):
    db.update({'balance':200})
    await ctx.send('Database rebooted. Balance are now set to $200.')


@bot.command()
async def slot(ctx, amount):
    userid = ctx.author.id
    amount = int(amount)
    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'balance':0})
        await ctx.send('Ở cái xã hội này phải chịu khó làm, chịu khó học hỏi, khắc có tiền. Nay không kiếm được nhiều thì kiếm được ít, mình tích tiểu thành đại, mình chưa có thì mình không được chơi bời. Mình chưa có thì mình đừng có ăn chơi lêu lổng, đừng có a dua a tòng, đàn đúm.\n     -anh Huấn - 2020.')

    # look for the user object
    user_db_obj = db.search(database.id == userid)[0]
    # extract the balance from the user object
    user_balance = float(str(user_db_obj).split()[-1][:-1])

    if user_balance == 0 or amount>user_balance or amount <= 0:
        message = 'Không có tiền mà đòi đánh bạc? Người không chơi là ngưòi thắng.'
    
    else:
        multiplier = 0
        values = ['orange', 'banana', 'grape', 'pineapple', 'coin']
        emoji_dict = {'orange':'🍊', 'banana':'🍌', 'grape':'🍇', 'pineapple':'🍍', 'coin':'💰'}
        output = []
        for i in range(3):
            output += [random.choice(values)]
        if output[0] == output[1] and output[0] == output[2]:
            if output[0] == 'coin':
                multiplier = 5
            else:
                multiplier = 3
        elif output[0] == output[1] or output[1] == output[2] or output[0] == output[2]:
            if output.count('coin') == 2:
                multiplier = 2.5
            else:
                multiplier = 2
        elif 'coin' in output:
            multiplier = 0.5
        else:
            multiplier = 0

        for i in range(len(output)):
            output[i] = emoji_dict[output[i]]
        
        slot_output = '|  {}  |  {}  |  {}  |'.format(output[0], output[1], output[2])

        if multiplier == 0:
            message = 'Chúc mừng, bạn đã mất hết tiền. Người không chơi là người thắng.'
        if multiplier == 0.5:
            message = 'Chúc may mắn lần sau, bạn được hoàn lại 1 nửa số tiền (x0.5).'
        else:
            message = 'Đánh bạc thành công, bạn đã x{} số tiền bỏ ra (${}).'.format(multiplier, amount)
        
        user_balance = user_balance - amount
        db.update({'balance':user_balance}, database.id == userid)
        amount = amount*multiplier
        user_balance += amount
        db.update({'balance':user_balance}, database.id == userid)

        embed=discord.Embed(title='', color=0x07edea)
        embed.add_field(name='FEELING LUCKY KID?', value='.', inline=False)
        embed.add_field(name=slot_output, value=message, inline=False)
        embed.set_footer(text="Số dư hiện tại: ${}".format(user_balance))
        await ctx.send(embed=embed)

