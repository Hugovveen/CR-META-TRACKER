import json
from collections import Counter

# ----------- LOAD DATA --------------------
with open("db/opponent_decks.json", "r") as f:
    data = json.load(f)

total_decks = len(data)
raw_counter = Counter()
deck_counter = Counter()

# ----------- COUNTING ----------------------
for battle_time, deck in data.items():
    seen = set()
    for card_name in deck.keys():
        raw_counter[card_name] += 1
        seen.add(card_name)
    for c in seen:
        deck_counter[c] += 1

total_raw = sum(raw_counter.values())

# ----------- FUNCTION ----------------------
def stats(card):
    if card not in raw_counter:
        return None
    
    raw = raw_counter[card]
    decks = deck_counter[card]
    return {
        "card": card,
        "raw_count": raw,
        "raw_%": round(100 * raw / total_raw, 2),
        "deck_count": decks,
        "deck_%": round(100 * decks / total_decks, 2),
    }

# ----------- ORACLE LOOP -------------------
print("Clash Royale Oracle – type a card name, or 'exit' to quit.")
print(f"Loaded {total_decks} decks.\n")

while True:
    card = input("Card >> ").strip()
    if card.lower() == "exit":
        break
    
    info = stats(card)
    if info is None:
        print("No data for that card.\n")
        continue
    
    print(f"\nCard: {info['card']}")
    print(f"  Raw count     : {info['raw_count']}")
    print(f"  Raw frequency : {info['raw_%']} %")
    print(f"  Deck count    : {info['deck_count']} / {total_decks}")
    print(f"  Deck playrate : {info['deck_%']} %\n")
