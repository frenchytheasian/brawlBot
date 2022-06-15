from pprint import pprint

import brawlstats
from discord.ext import commands

from credentials import DISCORD_TOKEN, BRAWL_TOKEN
from helpers import read_json
from database import get_reset_time

MYCLUB = 'VCVQPP2'

client = brawlstats.Client(token=BRAWL_TOKEN())
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():

    print(
        f'{bot.user} is connected!'
    )


@bot.command(name="get_battle_logs", help="Get the battle logs for a player")
async def get_battle_logs(ctx, player_tag):
    logs = client.get_battle_logs(player_tag)
    await ctx.send(logs)


@bot.command(name="get_club_stats", help="Get the club stats")
async def get_club_stats(ctx):
    club = client.get_club(MYCLUB)
    message = f"""Name : {club.name}\n
    Description : {club.description}\n
    Type : {club.type}\n
    Trophies : {club.trophies}\n
    Required trophies : {club.required_trophies}\n"""
    await ctx.send(message)


@bot.command(name="get_club_members", help="Get the members of the club")
async def get_club_members(ctx):
    members = client.get_club(MYCLUB).members
    message = "\n".join(member.name for member in members)
    await ctx.send(message)


@bot.command(name="trophy_movers", help="Get the trophy movers for the club. Data is reset whenever Michael gets to it")
async def trophy_movers(ctx):
    members = client.get_club(MYCLUB).members
    old_data = read_json()

    message = f"Trophy movement since {get_reset_time()}:\n\n"

    for i, member in enumerate(members):
        print(f"{i}/{len(members)}")
        player = client.get_player(member.tag)
        
        current_trophies = player.trophies
        old_trophies = old_data["data"][i]["trophies"]
        trophy_diff = current_trophies - old_trophies
        
        arrow = ""
        if trophy_diff > 0:
            arrow = "⬆"
            message += f"{member.name}: {current_trophies} {trophy_diff} {arrow}\n"
        elif trophy_diff < 0:
            arrow = "⬇"
            message += f"{member.name}: {current_trophies} {trophy_diff} {arrow}\n"
        else:
            continue
        
    
    await ctx.send(message)


bot.run(DISCORD_TOKEN())

if __name__ == "__main__":
    pass
