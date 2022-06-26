import firebase_admin
from firebase_admin import firestore
from typing import Dict
from datetime import date, datetime
import json
import requests

from credentials import BRAWL_TOKEN, FIRESTORE_CRED


MYCLUB = '%23VCVQPP2'

headers = {'Authorization': f'Bearer {BRAWL_TOKEN()}'}

firebase_admin.initialize_app(FIRESTORE_CRED())

db = firestore.client()


def get_data():
    players = dict()
    players["data"] = []

    url = f'https://bsproxy.royaleapi.dev/v1/clubs/{MYCLUB}/members'
    response = json.loads(requests.get(url, headers=headers).text)
    members = response['items']
    for member in members:
        player_tag = '%23' + member['tag'][1:]
        url = f'https://bsproxy.royaleapi.dev/v1/players/{player_tag}'
        player = json.loads(requests.get(url, headers=headers).text)

        player_info = dict()
        player_info["tag"] = player["tag"]
        player_info["name"] = player["name"]
        player_info["trophies"] = player["trophies"]

        players["data"].append(player_info)

    return players


def update_db(data: Dict = get_data()):
    today = date.today().strftime("%m%d%Y")
    data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc_ref = db.collection('daily_stats').document(today)
    response = doc_ref.set(data)
    print(response)


def read_db():
    today = date.today().strftime("%m%d%Y")
    stats_ref = db.collection('daily_stats').document(today)
    doc = stats_ref.get()
    return doc.to_dict()


if __name__ == "__main__":
    print(read_db())
