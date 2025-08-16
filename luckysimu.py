import tkinter as tk
import random
import json
import math
import os

SAVE_FILE = "save.json"

# =============================
# Game State
# =============================
state = {
    "luck": 1,
    "LP": 0,
    "PP": 0,
    "TP": 0,
    "best_rarity": 0
}

# =============================
# Helper Functions
# =============================
def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            state.update(data)

def calc_luck():
    """Calculate effective luck with boosts."""
    lp_boost = state["LP"] * 2
    pp_boost = max(1, math.ceil(state["PP"]**0.5))
    tp_boost = 1 + math.ceil(state["TP"]**(3/4))
    return max(1, (1 + lp_boost) ** pp_boost * tp_boost)

def rarity_chance(rarity):
    """Base chance (rarity 1 = 1/2, rarity 2 = 1/4, etc)."""
    return 1 / (2 ** rarity)

def get_actual_chance(rarity):
    return calc_luck() * rarity_chance(rarity)

def roll_rarity():
    """Roll for rarity using actual chance rules."""
    for rarity in range(100, 0, -1):
        if get_actual_chance(rarity) >= 1:
            continue
        if random.random() < get_actual_chance(rarity):
            return rarity
    return 1

def preview_gains():
    """Preview how many LP/PP/TP would be gained if reset now."""
    best = state["best_rarity"]
    lp_gain = max(0, best)
    pp_gain = max(0, best // 15)
    tp_gain = max(0, best // 30)
    return lp_gain, pp_gain, tp_gain

def reset_LP():
    best = state["best_rarity"]
    if best > 0:
        state["LP"] += best
        state["best_rarity"] = 0

def reset_PP():
    best = state["best_rarity"]
    if best >= 15:
        state["PP"] += best // 15
        state["LP"] = 0
        state["best_rarity"] = 0

def reset_TP():
    best = state["best_rarity"]
    if best >= 30:
        state["TP"] += best // 30
        state["PP"] = 0
        state["LP"] = 0
        state["best_rarity"] = 0

# =============================
# GUI Functions
# =============================
def do_roll():
    rarity = roll_rarity()
    state["best_rarity"] = max(state["best_rarity"], rarity)
    update_labels()
    save_game()

def do_reset(event=None):
    reset_LP()
    update_labels()
    save_game()

def do_prestige(event=None):
    reset_PP()
    update_labels()
    save_game()

def do_transcend(event=None):
    reset_TP()
    update_labels()
    save_game()

def update_labels():
    lp_gain, pp_gain, tp_gain = preview_gains()
    stats_label.config(text=(
        f"Luck: {calc_luck():.2f}\n"
        f"LP: {state['LP']} (+{lp_gain})\n"
        f"PP: {state['PP']} (+{pp_gain})\n"
        f"TP: {state['TP']} (+{tp_gain})\n"
        f"Best Rarity: {state['best_rarity']}"
    ))

# =============================
# Setup GUI
# =============================
root = tk.Tk()
root.title("Luck Simulator")

roll_button = tk.Button(root, text="Roll", command=do_roll, width=20, height=2)
roll_button.pack(pady=10)

stats_label = tk.Label(root, text="", font=("Arial", 14))
stats_label.pack(pady=10)

root.bind("w", do_reset)
root.bind("e", do_prestige)
root.bind("r", do_transcend)

load_game()
update_labels()
root.mainloop()
