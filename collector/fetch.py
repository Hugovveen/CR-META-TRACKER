from dotenv import load_dotenv
import requests
import os
import urllib.parse as up
import json

load_dotenv()
key = os.getenv('key')

player_tag = "#2RJ0LJYCU"
encoded_tag = up.quote(player_tag)

url = f'https://api.clashroyale.com/v1/players/{encoded_tag}/battlelog'

headers = {
    "Authorization": f'Bearer {key}'
}

response = requests.get(url, headers=headers)
parsed = response.json()

faced_opponents  = {}

#TODO UPDATE LEVELS ZODAT ZE KLOPPEN MET RARITY BONUS

for i in range(len(parsed)):
    battle = parsed[i]
    battle_time = battle["battleTime"]
    decks = {}
    for k in range(len(battle['opponent'][0]['cards'])):
        card_name = battle["opponent"][0]["cards"][k]['name']
        card_level = battle["opponent"][0]["cards"][k]['level']
        ecost = battle["opponent"][0]["cards"][k]['elixirCost']
        card_rarity = battle["opponent"][0]["cards"][k]['rarity']
        decks[card_name] = {'level':card_level, 'elixir':ecost, 'rarity':card_rarity}
    faced_opponents[battle_time] = (decks)

with open("db/opponent_decks", "w") as f:
    json.dump(faced_opponents, f, indent=4)
print("Data is opgeslagen kanker nerd")

