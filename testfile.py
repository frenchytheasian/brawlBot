from staticip import get_proxy
from credentials import DISCORD_TOKEN, BRAWL_TOKEN

import requests
import json

MYCLUB = '%23VCVQPP2'

headers = {'Authorization': f'Bearer {BRAWL_TOKEN()}'}

url = f'https://api.brawlstars.com/v1/clubs/{MYCLUB}/members'
    
r = requests.get(url, proxies=get_proxy(), headers=headers)
print(r.text)
print(type(json.loads(r.text)))
