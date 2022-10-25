import datetime
import json
from pprint import pprint

import requests
from discord.ext import commands

from credentials import DISCORD_TOKEN, BRAWL_TOKEN
from database import read_daily_stats_db, create_tag, read_tag

MYCLUB = '%23VCVQPP2'

headers = {'Authorization': f'Bearer {BRAWL_TOKEN()}'}

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f'{date}: {bot.user} is connected!'
    )


@bot.command(name="trophy_movers", help="Get the trophy movers for the club. Data is reset daily")
async def trophy_movers(ctx):
    await ctx.send('Loading Data...')

    old_data = read_daily_stats_db()

    message = f"Trophy movement since {old_data['last_updated']}:\n\n"
    stats = []
    members = old_data["data"]

    for member in enumerate(members):
        member = member[1]
        player_tag = '%23' + member['tag'][1:]
        url = f'https://bsproxy.royaleapi.dev/v1/players/{player_tag}'

        player = json.loads(requests.get(url, headers=headers).text)

        current_trophies = player["trophies"]
        old_trophies = member['trophies']
        trophy_diff = current_trophies - old_trophies

        arrow = ""
        if trophy_diff > 0:
            arrow = "⬆"
            stats.append(
                (f"{member['name']}: {current_trophies} {trophy_diff} {arrow}\n", trophy_diff))
        elif trophy_diff < 0:
            arrow = "⬇"
            stats.append(
                (f"{member['name']}: {current_trophies} {trophy_diff} {arrow}\n", trophy_diff))
        else:
            continue

    stats = [member[0]
             for member in sorted(stats, key=lambda x: x[1], reverse=True)]
    message += "".join(stats)
    await ctx.send(message)


@bot.command(name="set_tag", help="Connect your brawl stars tag to your discord account")
async def set_tag(ctx, tag):
    sender = ctx.message.author
    create_tag(str(sender), tag)
    await ctx.send(f"Tag: {tag} has been set for {sender}")


@bot.command(name="get_tag", help="Get your brawl stars tag")
async def get_tag(ctx):
    sender = ctx.message.author
    tag = read_tag(str(sender))
    await ctx.send(tag)


@bot.command(name="tag_lookup", help="Get a listing of player tags to find yours")
async def tag_lookup(ctx):
    url = f'https://bsproxy.royaleapi.dev/v1/clubs/{MYCLUB}/members'

    club = json.loads(requests.get(url, headers=headers).text)

    message = ""
    for player in club['items']:
        message += f"{player['name']}: {player['tag']}\n"
    await ctx.send(message)


def calculate_trophy_loss(trophies):
    if trophies <= 500:
        return 0
    elif trophies <= 524:
        return trophies % 25
    else:
        return trophies % 25 + 1


@bot.command(name="trophy_reset", help="Get the amount of trophies lost during trophy reset")
async def trophy_reset(ctx):
    sender = ctx.message.author
    tag = read_tag(str(sender))
    tag = '%23' + tag[1:]
    url = f'https://bsproxy.royaleapi.dev/v1/players/{tag}'

    player = json.loads(requests.get(url, headers=headers).text)
    try:
        player_brawlers = player['brawlers']
        player_trophies = player['trophies']
    except KeyError:
        await ctx.send(f"Unable to get statistics for {sender}.\n\nSet your tag first using the !set_tag <YOUR TAG> command")
        return

    total_trophy_loss = 0
    for brawler in player_brawlers:
        trophy_loss = calculate_trophy_loss(int(brawler['trophies']))
        total_trophy_loss += trophy_loss
        print(
            f'{brawler["name"]}: {brawler["trophies"]}, Losing {trophy_loss} trophies')

    await ctx.send(f'{player["name"]} is losing {total_trophy_loss} trophies at the end of the season to go from {player_trophies} to {player_trophies - total_trophy_loss} trophies')

bot.run(DISCORD_TOKEN())
