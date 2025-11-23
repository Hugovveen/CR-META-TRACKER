import os
import json
from collections import Counter
import plotly.express as px

# 1. JSON inladen
with open("analysis/opponent_decks.json", "r") as f:
    data = json.load(f)

# 2. Frequenties tellen
counter = Counter()

for battle_time, deck in data.items():
    for card_name, card_info in deck.items():
        counter[card_name] += 1

# 3. Omzetten naar dataframe-achtige structuur
cards = list(counter.keys())
counts = list(counter.values())

# 4. Plotly bar chart
fig = px.bar(
    x=cards,
    y=counts,
    labels={"x": "Card", "y": "Frequency"},
    title="Most encountered opponent cards"
)

fig.update_layout(
    xaxis_tickangle=-45,
    title_x=0.5,
    plot_bgcolor="#0a0f2c",
    paper_bgcolor="#0a0f2c",
    font=dict(color="white")
)

fig.write_html("plot.html")
