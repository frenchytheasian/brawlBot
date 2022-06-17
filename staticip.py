# Heroku generates dynamic IP addresses, but brawstars API needs a static IP.
import requests
import os

from dotenv import load_dotenv

def get_proxy():
    load_dotenv()

    proxies = {
        "http": os.environ['QUOTAGUARDSTATIC_URL'],
        "https": os.environ['QUOTAGUARDSTATIC_URL']
    }
    return proxies