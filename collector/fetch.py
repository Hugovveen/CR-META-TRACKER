from dotenv import load_dotenv
import requests
import os
import urllib.parse as up
import json

#ADMIN STUFF
#TODO
#KEY CHECKER DOES NOT WORK FIX THIS
#DOESNT RAISE ERROR EITHER
env_list = [
    #"keys/desktop_home.env",
    #"keys/uva.env",
    #"keys/weesper.env",
    'keys/uva-sp-c0.005.env'
]
player_tag = "#2RJ0LJYCU"
encoded_tag = up.quote(player_tag)
url = f'https://api.clashroyale.com/v1/players/{encoded_tag}/battlelog'


for k in env_list: 
    
    load_dotenv(k)  
    key = os.getenv("key")
    headers = {
    "Authorization": f'Bearer {key}'
        }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        break
    elif response.status_code == 403:
        continue
    else:
        raise Exception("no valid keys found:(")


parsed = response.json()

with open("db/opponent_decks.json", "r") as f:
    existing = json.load(f)

#TODO UPDATE LEVELS ZODAT ZE KLOPPEN MET RARITY BONUS

faced_opponents = {}
print("Existing battles in DB:", len(existing))

for i in range(len(parsed)):
    battle = parsed[i]
    battle_time = battle["battleTime"]

    if battle_time not in existing:
        print("NEW battle found:", battle_time)
        decks = {}

        cards = battle["opponent"][0]["cards"]

        for card in cards:
            card_name   = card.get("name")
            card_level  = card.get("level")
            ecost       = card.get("elixirCost")  
            card_rarity = card.get("rarity")

            decks[card_name] = {
                "level": card_level,
                "elixir": ecost,
                "rarity": card_rarity
            }

        faced_opponents[battle_time] = decks

for battle_time, deck in faced_opponents.items():
    existing[battle_time] = deck

with open("db/opponent_decks.json", "w") as f:
    json.dump(existing, f, indent=4)

#     json.dump(faced_opponents, f, indent=4)
#print(faced_opponents)
print("New battles this run:", len(faced_opponents))

for t, deck in faced_opponents.items():
    existing[t] = deck

print("Total battles after merge:", len(existing))

