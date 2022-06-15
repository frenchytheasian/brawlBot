import json
import datetime
from pprint import pprint

import brawlstats

from credentials import BRAWL_TOKEN

CLIENT = brawlstats.Client(token=BRAWL_TOKEN())
MYCLUB = "VCVQPP2"

class MetaData:
    reset_time = "14 Jun 2022, ~17:30 CDT"

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
        json.dump(players, outfile)
    MetaData.reset_time = datetime.datetime.now()
    
def get_reset_time():
    return MetaData.reset_time


if __name__ == "__main__":
    build_json()
        
    
        