import json
from collections import Counter
import plotly.express as px
import pandas as pd


with open("db/opponent_decks.json", "r") as f:
    data = json.load(f)

counter = Counter()

total_decks = len(data)


for battle_time, deck in data.items():
    for card_name, card_info in deck.items():
        counter[card_name] += 1

total_cards = sum(counter.values())
top10 = counter.most_common(10)

rows = []
for card, count in top10:
    raw_pct = (count / total_cards) * 100
    deck_pct = (count / total_decks) * 100
    rows.append({"card": card, "count": count, "raw_%":raw_pct, "deck_%":deck_pct})

df = pd.DataFrame(rows)
df = df.sort_values("deck_%", ascending=False)

fig = px.bar(
    df,
    x="card",
    y="deck_%",
    hover_data=["count", "raw_%", "deck_%"],
    title="Top 10 meest voorkomende kaarten (deck-playrate)",
    labels={"card": "Kaart", "deck_%": "Deck playrate (%)"}
)

# Optioneel: percentages als label boven de bars
fig.update_traces(
    text=df["deck_%"].round(1).astype(str) + "%",
    textposition="outside"
)

fig.update_layout(
    xaxis_tickangle=-45,
    title_x=0.5,
    plot_bgcolor="#0a0f2c",
    paper_bgcolor="#0a0f2c",
    font=dict(color="white"),
    margin=dict(l=40, r=40, t=80, b=120)
)

fig.write_html("plot_4.1_top10.html")
