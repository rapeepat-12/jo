import tkinter as tk
import random
import math
import json
import os

SAVE_FILE = "game_save.json"

# ==== Number Formatting with Suffix ====
suffixes = ["", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp", "Oc", "No", "De", 
            "Vt", "Tg", "qg", "Qg", "sg", "Sg", "Og", "Ng", "Ce"]

def format_number(n):
    if n < 1000:
        return str(n)
    magnitude = 0
    while abs(n) >= 1000 and magnitude < len(suffixes)-1:
        magnitude += 1
        n /= 1000.0
    return f"{n:.2f}{suffixes[magnitude]}"

# ==== Game State ====
state = {
    "best_rarity": 1,
    "LP": 0,
    "PP": 0,
    "TP": 0,
    "Rp": 0,
    "luck": 1
}

# ==== Save & Load ====
def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            state.update(data)

load_game()

# ==== Rarity Generator ====
RARITY_CAP = 100000

def rarity_chance(index):
    return 1 / (2 ** (index - 1))

def roll_rarity():
    luck = calc_luck()
    chosen = 1
    for r in range(1, RARITY_CAP + 1):
        chance = luck * rarity_chance(r)
        if chance < 1:
            chosen = r
        else:
            break
    return chosen

# ==== Boost System ====
def calc_luck():
    base = 1
    lp = state["LP"]
    pp = state["PP"]
    tp = state["TP"]
    rp = state["Rp"]

    luck = base
    # LP effect
    luck *= (lp * 2 + 1)

    # PP effect
    if pp > 0:
        luck *= math.ceil(pp ** 0.5)

    # TP effect
    if tp > 0:
        luck *= math.ceil(3/4)

    # Rp effect
    if rp > 0:
        luck *= rp

    return max(1, luck)

def calc_lp_boost():
    return state["LP"] * 2 + 1

def calc_pp_boost():
    return 2 if state["PP"] > 0 else 1

def calc_tp_boost():
    return 1 + math.ceil(state["TP"] ** (2/3)) if state["TP"] > 0 else 1

def calc_rp_boost():
    return 1 + state["Rp"]/10

# ==== Reset Functions ====
def reset_lp():
    gained = state["best_rarity"] - 1
    state["LP"] += gained
    state["best_rarity"] = 1
    update_labels()
    save_game()

def reset_pp():
    if state["best_rarity"] >= 15:
        gained = state["best_rarity"] // 15
        state["PP"] += gained
        state["LP"] = 0
        state["best_rarity"] = 1
        update_labels()
        save_game()

def reset_tp():
    if state["best_rarity"] >= 30:
        gained = state["best_rarity"] // 30
        state["TP"] += gained
        state["PP"] = 0
        state["LP"] = 0
        state["best_rarity"] = 1
        update_labels()
        save_game()

def reset_rp():
    if state["best_rarity"] >= 100:
        gained = state["best_rarity"] // 100
        state["Rp"] += gained
        state["TP"] = 0
        state["PP"] = 0
        state["LP"] = 0
        state["best_rarity"] = 1
        update_labels()
        save_game()

# ==== UI ====
root = tk.Tk()
root.title("Luck Simulator Expanded")

rarity_label = tk.Label(root, text="Rarity: 1")
rarity_label.pack()

luck_label = tk.Label(root, text="Luck: 1")
luck_label.pack()

point_label = tk.Label(root, text="LP: 0 PP: 0 TP: 0 Rp: 0")
point_label.pack()

def roll():
    rarity = roll_rarity()
    if rarity > state["best_rarity"]:
        state["best_rarity"] = rarity
    update_labels()
    save_game()

def update_labels():
    rarity_label.config(text=f"Rarity: {format_number(state['best_rarity'])}")
    luck_label.config(text=f"Luck: {format_number(calc_luck())}")
    point_label.config(text=f"LP: {format_number(state['LP'])} "
                            f"PP: {format_number(state['PP'])} "
                            f"TP: {format_number(state['TP'])} "
                            f"Rp: {format_number(state['Rp'])}")

roll_button = tk.Button(root, text="Roll", command=roll)
roll_button.pack()

root.bind("w", lambda e: reset_lp())
root.bind("e", lambda e: reset_pp())
root.bind("r", lambda e: reset_tp())
root.bind("t", lambda e: reset_rp())

update_labels()
root.mainloop()
