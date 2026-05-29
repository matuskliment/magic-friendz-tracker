#!/usr/bin/env python3
"""Generate showroom match CSV for Magic Friendz Tracker import."""

import csv
import random
from datetime import date, timedelta

random.seed(42)

PLAYERS = [
    "Alex Carter",
    "RampItUp99",
    "Marcus Webb",
    "GoWideOrGoHome",
    "Devin Okonkwo",
    "DemonicTutor",
    "Liam Foster",
    "StaxAndRelax",
    "Carlos Mendez",
    "BlueEnvy",
    "Hannah Berg",
    "MillItAll",
    "Lucy Tran",
    "TapThatPlains",
    "Zara Idris",
]

DECKS = [
    "The Ur-Dragon",
    "Edgar Markov",
    "Y'shtola, Night's Blessed",
    "Atraxa, Praetors' Voice",
    "Krenko, Mob Boss",
    "Kaalia of the Vast",
    "Sauron, the Dark Lord",
    "Ms. Bumbleflower",
    "Pantlaza, Sun-Favored",
    "Vivi Ornitier",
    "Teval, the Balanced Scale",
    "Lathril, Blade of the Elves",
    "Giada, Font of Hope",
    "The Wise Mothman",
    "Yuriko, the Tiger's Shadow",
    "Fire Lord Azula",
    "Jodah, the Unifier",
    "Kenrith, the Returned King",
    "Nekusar, the Mindrazer",
    "Ulalek, Fused Atrocity",
    "Baylen, the Haymaker",
    "Isshin, Two Heavens as One",
    "Valgavoth, Harrower of Souls",
    "Miirym, Sentinel Wyrm",
    "Toph, the First Metalbender",
    "Chatterfang, Squirrel General",
    "Kefka, Court Mage",
    "Bello, Bard of the Brambles",
    "Sephiroth, Fabled SOLDIER",
    "Cloud, Ex-SOLDIER",
    "Hearthhull, the Worldseed",
    "The Necrobloom",
    "Esika, God of the Tree",
    "Hakbal of the Surging Soul",
    "Hashaton, Scarab's Fist",
    "Muldrotha, the Gravetide",
    "Flubs, the Fool",
    "Frodo, Adventurous Hobbit // Sam, Loyal Attendant",
    "Animar, Soul of Elements",
    "Glarb, Calamity's Augur",
    "Ygra, Eater of All",
    "Arcades, the Strategist",
    "Rin and Seri, Inseparable",
    "Wilhelt, the Rotcleaver",
    "Caesar, Legion's Emperor",
    "Mr. House, President and CEO",
    "Aragorn, the Uniter",
    "Breya, Etherium Shaper",
    "Meren of Clan Nel Toth",
    "Zhulodok, Void Gorger",
    "Ashling, the Limitless",
    "Gishath, Sun's Avatar",
    "Teysa Karlov",
    "Oloro, Ageless Ascetic",
    "Arabella, Abandoned Doll",
    "Shorikai, Genesis Engine",
    "Korvold, Fae-Cursed King",
    "Go-Shintai of Life's Origin",
    "K'rrik, Son of Yawgmoth",
    "Ghyrson Starn, Kelermorph",
    "Kinnan, Bonder Prodigy",
    "Tom Bombadil",
    "Atla Palani, Nest Tender",
    "Ezio Auditore da Firenze",
    "Urza, Lord High Artificer",
    "Xyris, the Writhing Storm",
    "Helga, Skittish Seer",
    "Zaxara, the Exemplary",
    "Ureni of the Unwritten",
    "The First Sliver",
    "Voja, Jaws of the Conclave",
    "Zurgo Stormrender",
    "Zinnia, Valley's Voice",
    "Eriette of the Charmed Apple",
    'Henzie "Toolbox" Torre',
    "Maralen, Fae Ascendant",
    "Kuja, Genome Sorcerer",
    "Omnath, Locus of Creation",
    "Sidar Jabari of Zhalfir",
    "Sisay, Weatherlight Captain",
]

NOTES = [
    "Close game — board wipe into lethal.",
    "Salt levels high after turn 3 Cyclonic Rift.",
    "New player borrowed this deck for the night.",
    "Mulliganed to five, still won.",
    "Politics table — everyone ganged up on the archenemy.",
    "Combo line on turn 9 sealed it.",
    "Grindy value game, went to 2 hours.",
    "Someone forgot their trigger — table ruled charitably.",
    "First match of the night.",
    "Last match before pizza break.",
    "Upset of the evening.",
    "Stax player got eliminated first for once.",
    "Three-player pod after someone had to leave early.",
    "Double mulligan meta.",
    "Epic top-deck moment.",
    "",
    "",
    "",
    "",
]

WINNING_CARDS = [
    "Cyclonic Rift",
    "Craterhoof Behemoth",
    "Thassa's Oracle",
    "Torment of Hailfire",
    "Expropriate",
    "Triumph of the Hordes",
    "Vito, Thorn of the Dusk Rose",
    "Laboratory Maniac",
    "Purphoros, God of the Forge",
    "Rise of the Dark Realms",
]

CORE_DECKS = DECKS[:40]
DECK_OWNERS = {deck: random.choice(PLAYERS) for deck in DECKS}
deck_first_seen = set()

player_signatures = {}
available = CORE_DECKS.copy()
random.shuffle(available)
for i, player in enumerate(PLAYERS):
    player_signatures[player] = [
        available[i % len(available)],
        available[(i + 7) % len(available)],
    ]


def pick_deck_for_player(player, used_decks, force_signature=False):
    if random.random() < 0.12:
        unused = [d for d in DECKS if d not in deck_first_seen and d not in used_decks]
        if unused:
            return random.choice(unused)
    if force_signature or random.random() < 0.55:
        return random.choice(player_signatures[player])
    if random.random() < 0.7:
        return random.choice(CORE_DECKS)
    return random.choice(DECKS)


def assign_deck_to_player(player, pod_players, used_decks, force_signature=False):
    for _ in range(25):
        deck = pick_deck_for_player(player, used_decks, force_signature=force_signature)
        if deck in used_decks:
            continue
        if deck not in deck_first_seen:
            owner = DECK_OWNERS[deck]
            if owner not in pod_players or owner != player:
                continue
        return deck
    for deck in player_signatures[player]:
        if deck not in used_decks:
            return deck
    for deck in CORE_DECKS:
        if deck not in used_decks:
            return deck
    unused = [d for d in DECKS if d not in used_decks]
    return random.choice(unused or DECKS)


def pod_sizes_for_80():
    sizes = [4] * 56
    remainder = [3] * 10 + [5] * 10 + [2] * 4
    random.shuffle(remainder)
    return sizes + remainder


def session_dates(count):
    start = date(2024, 9, 7)
    end = date(2025, 5, 24)
    span_days = (end - start).days
    dates = sorted(
        {start + timedelta(days=round(i * span_days / max(count - 1, 1))) for i in range(count)}
    )
    return dates


def distribute_matches_to_dates(num_matches, dates):
    assignment = []
    date_idx = 0
    while len(assignment) < num_matches:
        per_session = random.choice([2, 3, 3, 4])
        for _ in range(per_session):
            if len(assignment) >= num_matches:
                break
            assignment.append(dates[date_idx % len(dates)])
        date_idx += 1
    return assignment


def build_match(match_date, pod_size, match_num):
    participants = random.sample(PLAYERS, pod_size)
    entries = []
    used_decks = set()

    for p in participants:
        deck = assign_deck_to_player(
            p, participants, used_decks, force_signature=(match_num % 5 == 0)
        )
        used_decks.add(deck)
        if deck not in deck_first_seen:
            deck_first_seen.add(deck)
        entries.append((p, deck))

    weights = []
    for pilot, deck in entries:
        w = 1.0
        if deck in player_signatures.get(pilot, []):
            w += 0.35
        if pilot in ("Alex Carter", "Marcus Webb", "Hannah Berg"):
            w += 0.15
        weights.append(w)

    winner_idx = random.choices(range(len(entries)), weights=weights, k=1)[0]
    winner_deck = entries[winner_idx][1]
    winner_entry = entries[winner_idx]
    others = [e for i, e in enumerate(entries) if i != winner_idx]
    ordered = [winner_entry] + others

    while len(ordered) < 5:
        ordered.append(("", ""))

    note = random.choice(NOTES)
    if random.random() < 0.25:
        cards = random.sample(WINNING_CARDS, k=random.randint(1, 3))
        while len(cards) < 4:
            cards.append("")
    else:
        cards = ["", "", "", ""]

    duration = random.choice([75, 85, 90, 95, 100, 105, 110, 120, 125, 135, 150])

    return [
        match_date.isoformat(),
        ordered[0][0],
        ordered[0][1],
        ordered[1][0],
        ordered[1][1],
        ordered[2][0],
        ordered[2][1],
        ordered[3][0],
        ordered[3][1],
        ordered[4][0],
        ordered[4][1],
        winner_deck,
        note,
        cards[0],
        cards[1],
        cards[2],
        cards[3],
        str(duration),
    ]


def main():
    sizes = pod_sizes_for_80()
    random.shuffle(sizes)
    dates_pool = session_dates(24)
    match_dates = distribute_matches_to_dates(80, dates_pool)

    header = [
        "Date",
        "P1 (Win)",
        "D1 (Win)",
        "P2",
        "D2",
        "P3",
        "D3",
        "P4",
        "D4",
        "P5",
        "D5",
        "Winner",
        "Notes",
        "Card1",
        "Card2",
        "Card3",
        "Card4",
        "DurationMinutes",
    ]

    rows = [header]
    for i, (md, ps) in enumerate(zip(match_dates, sizes)):
        rows.append(build_match(md, ps, i))

    rows[1:] = sorted(rows[1:], key=lambda r: (r[0], r[1]))

    output_path = "showroom-matches.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

    four_player = sum(1 for s in sizes if s == 4)
    print(f"Wrote {len(rows) - 1} matches to {output_path}")
    print(
        f"Pod breakdown: 4p={sum(1 for s in sizes if s == 4)}, "
        f"3p={sum(1 for s in sizes if s == 3)}, "
        f"5p={sum(1 for s in sizes if s == 5)}, "
        f"2p={sum(1 for s in sizes if s == 2)}"
    )
    print(f"4-player rate: {four_player / 80 * 100:.1f}%")
    print(f"Unique decks used: {len(deck_first_seen)}")
    print(f"Date range: {min(match_dates)} to {max(match_dates)}")


if __name__ == "__main__":
    main()
