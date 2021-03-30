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
from tinydb import TinyDB, Query
import random


from test import *

token = 'NzYwMDAyNTY3ODc4MzQ0NzE1.X3FtjA.xH_Yv5vWtMS-N8cBxk_Idl1zWHU'
client = commands.Bot(command_prefix=';')

nums = '1\N{variation selector-16}\N{combining enclosing keycap}'

# process the custom database
db = TinyDB('database/currencydb.json')
database = Query()

# each member will be store in the data base under the
# form 'userid balance' seperated by a space
def read_database():
    with open('currencydb.txt', 'r') as file:
        database_raw = file.read().split('\n')
        database = {}
        for user in database:
            pass

# Custom help message - to be done
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("Đéo có help command đâu.")

@client.event
async def on_command_error(ctx, error):
    if type(error) == discord.ext.commands.errors.CommandOnCooldown:
        await ctx.send('Có làm thì mới có ăn. Chỉ nhận được lương 1 lần trong 10 phút.')

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
    
    summoners_icon, rank_solo, win, loss, winrate = get_solo_rank(profile)

    ranked_solo_line = '\n\n\nRanked Solo: {0:<10}\n\n'.format(rank_solo)
    win_loss_line = '\n\n\nWin - Loss: {}W {}L\n\n'.format(win, loss)
    winrate_line = 'Winrate: {0:>20}%\n\n'.format(winrate)

    comment = '\n\n'
    if winrate < 46:
        comment = 'Winrate thấp, rác vcl'
    if winrate >= 46 and winrate < 49:
        comment = 'Dưới trung bình, còn cần cố gắng'
    if winrate >=49 and winrate < 52:
        comment = 'Winrate trung bình, không có gì đặc sắc'
    if winrate >= 52:
        comment = 'Winrate cao, chắc chắn hack, target ban tướng của nó, report Riot pls'

    if win+loss >= 500:
        comment += '. Chơi nhiều vloz, get a life.'
    
    
    embed=discord.Embed(title=username, color=0x07edea)
    embed.set_thumbnail(url="https:"+summoners_icon)
    embed.add_field(name=ranked_solo_line, value=win_loss_line+winrate_line+comment, inline=True)
    embed.set_footer(text="Powered by Chris P Bacon")
    await ctx.send(embed=embed)

@client.command()
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


@client.command()
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

@client.command()
async def balance(ctx):
    userid = ctx.author.id

    if len(db.search(database.id == userid)) == 0:
        db.insert({'id':userid, 'balance':0})

    # look for the user object
    user_db_obj = db.search(database.id == userid)[0]
    # extract the balance from the user object
    user_balance = float(str(user_db_obj).split()[-1][:-1])

    await ctx.send('Số dư trong tài khoản của bạn là ${}.'.format(user_balance))  

@client.command()
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

@client.command()
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

@client.command()
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

@client.command()
@commands.has_permissions(administrator=True)
async def reset_database(ctx):
    db.update({'balance':200})
    await ctx.send('Database rebooted. Balance are now set to $200.')


@client.command()
async def slot(ctx, amount):
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
        multiplier = 0
        values = ['orange', 'banana', 'grape', 'coin']
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
            multiplier = 1.5
        else:
            multiplier = 0
        


@client.command()
@commands.cooldown(1,3600)
async def testing(ctx):
    await ctx.send('the author of this message is {}'.format(ctx.author.name))


client.run(token)
    
