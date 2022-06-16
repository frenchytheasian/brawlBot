# Heroku generates dynamic IP addresses, but brawstars API needs a static IP.
import requests
import os

from dotenv import load_dotenv

def get_proxy():
    load_dotenv()

    proxies = {
        "http": os.getenv('QUOTAGUARDSTATIC_URL'),
        "https": os.getenv('QUOTAGUARDSTATIC_URL')
    }
    return proxies