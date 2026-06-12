import getpass
import os
from main import *

token = getpass.getpass('Discord bot token: ')
os.environ['FOOTBALL_API_KEY'] = getpass.getpass('Football API key (football-data.org): ')
bot.run(token)