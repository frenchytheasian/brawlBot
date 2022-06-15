import os

from dotenv import load_dotenv

def DISCORD_TOKEN():
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')

def BRAWL_TOKEN():
    load_dotenv()
    return os.getenv('BRAWL_TOKEN')