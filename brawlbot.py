from pprint import pprint
import datetime
import json

import requests
from discord.ext import commands

from credentials import DISCORD_TOKEN, BRAWL_TOKEN
from database import read_json
from staticip import get_proxy

MYCLUB = '%23VCVQPP2'

headers = {'Authorization': f'Bearer {BRAWL_TOKEN()}'}

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f'{date}: {bot.user} is connected!'
    )

@bot.command(name="trophy_movers", help="Get the trophy movers for the club. Data is reset whenever Michael gets to it")
async def trophy_movers(ctx):
    url = f'https://api.brawlstars.com/v1/clubs/{MYCLUB}/members'
    
    response = json.loads(requests.get(url, proxies=get_proxy(), headers=headers).text)
    members = response['items']
    old_data = read_json()

    message = f"Trophy movement since {old_data['last_updated']}:\n\n"
    stats = []

    for i, member in enumerate(members):
        player_tag = '%23' + member['tag'][1:]
        url = f'https://api.brawlstars.com/v1/players/{player_tag}'
        
        print(f"{i}/{len(members)}")
        player = json.loads(requests.get(url, proxies=get_proxy(), headers=headers).text)
        
        current_trophies = player["trophies"]
        old_trophies = old_data["data"][i]["trophies"]
        trophy_diff = current_trophies - old_trophies
        
        
        arrow = ""
        if trophy_diff > 0:
            arrow = "⬆"
            stats.append((f"{member['name']}: {current_trophies} {trophy_diff} {arrow}\n", trophy_diff))
        elif trophy_diff < 0:
            arrow = "⬇"
            stats.append((f"{member['name']}: {current_trophies} {trophy_diff} {arrow}\n", trophy_diff))
        else:
            continue
        
    stats = [member[0] for member in sorted(stats, key=lambda x: x[1], reverse=True)]
    message += "".join(stats)
    await ctx.send(message)


bot.run(DISCORD_TOKEN())
