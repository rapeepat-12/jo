import tkinter as tk
from tkinter import messagebox
import math
import json
import os

SAVE_FILE = "progress.json"
MAX_RARITY = 100_000

# ------------------------
# Stats
# ------------------------
stats = {
    "Luck": 1.0,
    "LP": 0,
    "PP": 0,
    "TP": 0,
    "RP": 0
}

best_rarity = 1

# ------------------------
# Save / Load
# ------------------------
def save_progress():
    data = {"stats": stats, "best_rarity": best_rarity}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_progress():
    global best_rarity
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            stats.update(data["stats"])
            best_rarity = data["best_rarity"]

# ------------------------
# Suffix Formatter
# ------------------------
suffixes = ["", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp", "Oc", "No"]

def format_number(n):
    if n < 1000:
        return str(int(n))
    k = 0
    while n >= 1000 and k < len(suffixes) - 1:
        n /= 1000.0
        k += 1
    return f"{n:.2f}{suffixes[k]}"

# ------------------------
# Core Roll System
# ------------------------
def roll_rarity():
    global best_rarity

    chosen_rarity = None
    for r in range(1, MAX_RARITY + 1):
        base_chance = 1 / (2 ** (r - 1))   # rarity scaling
        actual_chance = base_chance * stats["Luck"]
        if actual_chance < 1:
            chosen_rarity = r
            break

    if chosen_rarity is None:
        # if all rarities are guaranteed, push beyond best rarity
        chosen_rarity = best_rarity + 1

    if chosen_rarity > best_rarity:
        best_rarity = chosen_rarity

    update_labels()

# ------------------------
# Reset Systems
# ------------------------
def reset_w(event=None):
    global best_rarity
    gained = best_rarity - 1
    stats["LP"] += gained
    stats["Luck"] *= (1 + stats["LP"] * 2)
    best_rarity = 1
    update_labels()

def prestige_e(event=None):
    global best_rarity
    if best_rarity >= 15:
        gained = best_rarity // 15
        stats["PP"] += gained
        stats["LP"] = 0
        best_rarity = 1
        stats["Luck"] *= math.ceil(stats["PP"] ** 0.5)
        update_labels()
    else:
        messagebox.showinfo("Prestige", "Reach rarity 15 to Prestige.")

def transcend_r(event=None):
    global best_rarity
    if best_rarity >= 30:
        gained = best_rarity // 30
        stats["TP"] += gained
        stats["PP"] = 0
        stats["LP"] = 0
        best_rarity = 1
        stats["Luck"] *= math.ceil((1 + (stats["TP"] ** (3/4))))
        update_labels()
    else:
        messagebox.showinfo("Transcend", "Reach rarity 30 to Transcend.")

def reincarnate(event=None):
    global best_rarity
    if best_rarity >= 100:
        gained = best_rarity // 100
        stats["RP"] += gained
        stats["TP"] = 0
        stats["PP"] = 0
        stats["LP"] = 0
        best_rarity = 1
        # reincarnation boosts
        stats["Luck"] *= 1 + stats["RP"]
        update_labels()
    else:
        messagebox.showinfo("Reincarnate", "Reach rarity 100 to Reincarnate.")

# ------------------------
# UI Update
# ------------------------
def update_labels():
    stats_label.config(
        text=(
            f"Luck: {format_number(stats['Luck'])}\n"
            f"LP: {format_number(stats['LP'])}\n"
            f"PP: {format_number(stats['PP'])}\n"
            f"TP: {format_number(stats['TP'])}\n"
            f"RP: {format_number(stats['RP'])}"
        )
    )
    rarity_label.config(text=f"Best Rarity: {best_rarity}")
    save_progress()

# ------------------------
# GUI Setup
# ------------------------
root = tk.Tk()
root.title("Luck Simulator")

stats_label = tk.Label(root, text="", font=("Arial", 14))
stats_label.pack()

rarity_label = tk.Label(root, text="", font=("Arial", 14))
rarity_label.pack()

roll_button = tk.Button(root, text="Roll", command=roll_rarity, font=("Arial", 14))
roll_button.pack(pady=10)

# Keybinds
root.bind("w", reset_w)
root.bind("e", prestige_e)
root.bind("r", transcend_r)
root.bind("t", reincarnate)

# Load + Start
load_progress()
update_labels()
root.mainloop()
