import json
from collections import Counter
import plotly.express as px

with open("db/opponent_decks.json", "r") as f:
    data = json.load(f)

counter = Counter()

for battle_time, deck in data.items():
    for card_name, card_info in deck.items():
        counter[card_name] += 1

total_cards = sum(counter.values())
top10 = counter.most_common(10)

rows = []
for card, count in top10:
    pct = (count / total_cards) * 100
    rows.append({"card": card, "count": count, "raw_%":pct})

print(rows)
#print(top10)
#print(total_cards)
