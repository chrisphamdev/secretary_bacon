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
    summoners_icon = profile.findAll('img', {'class':'ProfileImage'})
    rank_solo_obj = profile.findAll('div', {'class':'TierRank'})
    for item in rank_solo_obj:
        rank_solo = item.text

    wins = profile.findAll('span', {'class':'wins'})
    for item in wins:
        win = int(item.text[:-1])
    
    losses = profile.findAll('span', {'class':'losses'})
    for item in losses:
        loss = int(item.text[:-1])

    winrate = win/(win+loss)
    winrate = round(winrate*100)
    
    return rank_solo, win, loss, winrate

def get_champions(profile):
    all_champions = profile.findAll('div', {'class':'ChampionBox Ranked'})
    top5_champions = []
    for champion in all_champions:
        champion_name = champion.findAll('div', {'class':'ChampionName'})
        for champion_name_class in champion_name:
            if len(top5_champions) == 5:
                break
            top5_champions += [champion_name_class.text.strip()]
    return top5_champions

def get_past_20_games(profile):
    most_played = profile.findAll('td', {'class':'MostChampion'})
    top3 = []
    for content in most_played:
        champs = content.findAll('div', {'class':'Content'})
        top3 += [champs]

    top3_simplified = []

    for champ in top3:
        print(champ)

profile = get_profile('Chrispy Bacon')
get_solo_rank(profile)