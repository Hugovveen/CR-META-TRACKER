import json
from collections import Counter
import plotly.express as px

# 1. JSON inladen
with open("db/opponent_decks.json", "r") as f:
    data = json.load(f)

# 2. Frequenties tellen
counter = Counter()

for battle_time, deck in data.items():
    for card_name, card_info in deck.items():
        counter[card_name] += 1

# 3. Gesorteerde lijst maken
sorted_items = counter.most_common()  # [('Knight', 28), ('Valkyrie', 23), ...]

cards = [item[0] for item in sorted_items]
counts = [item[1] for item in sorted_items]

# 4. Plotly bar chart
fig = px.bar(
    x=cards,
    y=counts,
    labels={"x": "Card", "y": "Frequency"},
    title="Most encountered opponent cards (sorted)"
)

fig.update_layout(
    xaxis_tickangle=-45,
    title_x=0.5,
    plot_bgcolor="#0a0f2c",
    paper_bgcolor="#0a0f2c",
    font=dict(color="white")
)

fig.write_html("plot_5_sorted.html")
