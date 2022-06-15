import json
import datetime
from pprint import pprint

import brawlstats

from credentials import BRAWL_TOKEN

CLIENT = brawlstats.Client(token=BRAWL_TOKEN())
MYCLUB = "VCVQPP2"

def _get_data():
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
    players = _get_data()
    with open("data/data.json", "w") as outfile:
        players["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json.dump(players, outfile)
        
def read_json():
    with open("data/data.json", "r") as infile:
        data = json.load(infile)
    return data
    


if __name__ == "__main__":
    build_json()
        
    
        