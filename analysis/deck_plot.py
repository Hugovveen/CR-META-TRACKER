import json
import pandas as pd
import plotly.express as px

# Load data
with open("db/opponent_decks.json", "r") as f:
    data = json.load(f)

def safe_elixir(x):
    return x if isinstance(x, (int, float)) else 0

# --- 1. Skeleton kaarten (win conditions) ---
SKELETONS = {
    "Hog Rider": "Hog Cycle",
    "Royal Giant": "RG",
    "Balloon": "LavaLoon",
    "Lava Hound": "LavaLoon",
    "Miner": "Miner Control",
    "Graveyard": "Graveyard",
    "X-Bow": "Siege",
    "Mortar": "Siege",
    "Mega Knight": "MK Control",
    "Giant": "Giant Beatdown",
    "Golem": "Golem Beatdown",
    "Electro Giant": "E-Giant",
}

# --- 2. Main spells ---
MAIN_SPELLS = [
    "Fireball", "Poison", "Rocket", "Lightning", "Arrows", "Zap",
    "The Log", "Snowball"
]

rows = []

for battle_time, deck in data.items():
    cards = list(deck.keys())

    # Determine archetype
    archetype = "Unknown"
    for card in cards:
        if card in SKELETONS:
            archetype = SKELETONS[card]
            break

    # Determine main spell
    main_spell = next((c for c in cards if c in MAIN_SPELLS), "None")

    # average elixir
    avg_elixir = sum(safe_elixir(deck[c]["elixir"]) for c in deck) / 8

    # bucket de elixir
    if avg_elixir <= 3.0:
        elixir_type = "Cycle"
    elif avg_elixir <= 3.8:
        elixir_type = "Midrange"
    else:
        elixir_type = "Heavy"

    rows.append({
        "archetype": archetype,
        "main_spell": main_spell,
        "elixir_type": elixir_type
    })

df = pd.DataFrame(rows)

fig = px.bar(
    df["archetype"].value_counts(),
    title="Most encountered archetypes",
    labels={"value": "Aantal decks", "index": "Archetype"}
)
fig.write_html('bar_archetype.html')
