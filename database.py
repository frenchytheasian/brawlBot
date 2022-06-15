import json
from pprint import pprint

import brawlstats

from credentials import BRAWL_TOKEN

CLIENT = brawlstats.Client(token=BRAWL_TOKEN())
MYCLUB = "VCVQPP2"

def get_data():
    players = dict()
    players["data"] = []
    
    members = CLIENT.get_club(MYCLUB).members
    for member in members:
        player = CLIENT.get_player(member.tag)
        player_info = dict()
        player_info["tag"] = player.tag
        player_info["name"] = player.name
        player_info["trophies"] = player.trophies
        
        players["data"].append(player_info)
    return players

def build_json():
    players = get_data()
    with open("data.json", "w") as outfile:
        json.dump(players, outfile)

if __name__ == "__main__":
    build_json()
    
        
    
        