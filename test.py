import bs4

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

import ssl

def get_profile(summoner_name):
    ssl._create_default_https_context = ssl._create_unverified_context

    player_name = summoner_name
    profile_url = 'https://oce.op.gg/summoner/userName='

    player_name = player_name.replace(' ', '+')
    player_name = player_name.replace("'", "%27")
    profile_url += player_name

    client = urllib.request.urlopen(profile_url)
    profile_html = client.read()
    client.close()

    profile_html_parsed = soup(profile_html, 'html.parser')
    return profile_html_parsed


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