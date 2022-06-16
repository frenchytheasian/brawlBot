from pprint import pprint
import datetime

import requests
from discord.ext import commands

from credentials import DISCORD_TOKEN, BRAWL_TOKEN
from database import read_json
from staticip import get_proxy

MYCLUB = 'VCVQPP2'

headers = {'Authorization': f'Bearer {BRAWL_TOKEN()}'}

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f'{date}: {bot.user} is connected!'
    )

# @bot.command(name="trophy_movers", help="Get the trophy movers for the club. Data is reset whenever Michael gets to it")
# async def trophy_movers(ctx):
#     members = client.get_club(MYCLUB).members
#     old_data = read_json()

#     message = f"Trophy movement since {old_data['last_updated']}:\n\n"

#     for i, member in enumerate(members):
#         print(f"{i}/{len(members)}")
#         player = client.get_player(member.tag)
        
#         current_trophies = player.trophies
#         old_trophies = old_data["data"][i]["trophies"]
#         trophy_diff = current_trophies - old_trophies
        
#         arrow = ""
#         if trophy_diff > 0:
#             arrow = "⬆"
#             message += f"{member.name}: {current_trophies} {trophy_diff} {arrow}\n"
#         elif trophy_diff < 0:
#             arrow = "⬇"
#             message += f"{member.name}: {current_trophies} {trophy_diff} {arrow}\n"
#         else:
#             continue
        
    
#     await ctx.send(message)


# bot.run(DISCORD_TOKEN())

if __name__ == "__main__":
    r = requests.get("https://api.brawlstars.com/v1/brawlers", proxies=get_proxy(), headers=headers)
    pprint(r.text)
