import bs4

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

import ssl


def get_solo_rank(profile):
    # obtain summoner's icon
    summoners_icon_obj = profile.findAll('img', {'class':'ProfileImage'})
    for icon in summoners_icon_obj:
        summoners_icon = icon['src']

    # obtain rank solo 
    rank_solo_obj = profile.findAll('div', {'class':'TierRank'})
    for item in rank_solo_obj:
        rank_solo = item.text

    # obtain wins
    wins = profile.findAll('span', {'class':'wins'})
    for item in wins:
        win = int(item.text[:-1])

    # obtain losses
    losses = profile.findAll('span', {'class':'losses'})
    for item in losses:
        loss = int(item.text[:-1])

    # calculate win rate
    winrate = win/(win+loss)
    winrate = round(winrate*100)
    return summoners_icon, rank_solo, win, loss, winrate