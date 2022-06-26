import os
from dotenv import load_dotenv
from firebase_admin import credentials


def DISCORD_TOKEN():
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')


def BRAWL_TOKEN():
    load_dotenv()
    return os.getenv('BRAWL_TOKEN')


def FIRESTORE_CRED():
    load_dotenv()
    cred = credentials.Certificate({
        "type": "service_account",
        'project_id': os.getenv('PROJECT_ID'),
        "private_key": os.getenv('FIRESTORE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('FIRESTORE_EMAIL'),
        "token_uri": "https://oauth2.googleapis.com/token",
    })
    return cred
