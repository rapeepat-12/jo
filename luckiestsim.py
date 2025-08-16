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
    "RP": 0,
    "best_rarity": 0
}

# =============================
# Helper Functions
# =============================
suffixes = ["", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp", "Oc", "No",
            "De", "Vt", "Tg", "qg", "Qg", "sg", "Sg", "Og", "Ng", "Ce"]

def format_number(num):
    """Format large numbers with suffixes."""
    if num < 1000:
        return str(num)
    exp = int(math.log10(num) // 3)
    if exp < len(suffixes):
        value = num / (1000 ** exp)
        return f"{value:.2f}{suffixes[exp]}"
    return f"{num:.2e}"

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            state.update(data)

def calc_luck():
    """Calculate effective luck with boosts and reincarnation."""
    lp_boost = state["LP"] * 2
    pp_boost = max(1, math.ceil(state["PP"]**0.5))
    tp_boost = 1 + math.ceil(state["TP"]**(3/4))
    reinc_boost = (1 + state["RP"] / 20)  # Rp scales luck slowly
    return max(1, (1 + lp_boost) ** (pp_boost ** (1 + state["RP"]/10)) *
                  (tp_boost * (1 + 0.1 * state["RP"])) * reinc_boost)

def rarity_chance(rarity):
    return 1 / (2 ** rarity)

def get_actual_chance(rarity):
    return calc_luck() * rarity_chance(rarity)

def roll_rarity():
    for rarity in range(100, 0, -1):
        if get_actual_chance(rarity) >= 1:
            continue
        if random.random() < get_actual_chance(rarity):
            return rarity
    return 1

def preview_gains():
    best = state["best_rarity"]
    lp_gain = max(0, best)
    pp_gain = max(0, best // 15)
    tp_gain = max(0, best // 30)
    rp_gain = max(0, best // 60)
    return lp_gain, pp_gain, tp_gain, rp_gain

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

def reset_RP():
    best = state["best_rarity"]
    if best >= 60:
        state["RP"] += best // 60
        state["TP"] = 0
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

def do_reincarnate(event=None):
    reset_RP()
    update_labels()
    save_game()

def update_labels():
    lp_gain, pp_gain, tp_gain, rp_gain = preview_gains()
    stats_label.config(text=(
        f"Luck: {format_number(calc_luck()):>}\n"
        f"LP: {format_number(state['LP'])} (+{format_number(lp_gain)})\n"
        f"PP: {format_number(state['PP'])} (+{format_number(pp_gain)})\n"
        f"TP: {format_number(state['TP'])} (+{format_number(tp_gain)})\n"
        f"RP: {format_number(state['RP'])} (+{format_number(rp_gain)})\n"
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

root.bind("w", do_reset)        # LP reset
root.bind("e", do_prestige)     # PP reset
root.bind("r", do_transcend)    # TP reset
root.bind("t", do_reincarnate)  # RP reset

load_game()
update_labels()
root.mainloop()
