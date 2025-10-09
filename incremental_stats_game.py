#!/usr/bin/env python3
# Incremental Stats Game v3 🧮 GUI Edition
# Click buttons instead of typing commands

import math
import tkinter as tk
from tkinter import ttk

class Game:
    def __init__(self):
        self.stats = {"a": 10.0}
        self.unlocked = ["a"]
        self.all_boost = 1
        self.a_boost = 1
        self.upgrade_price = 100
        self.unlock_cost = 100
        self.challenge_level = 0
        self.challenge_active = False

    def tick(self):
        gains = {k: 0 for k in self.stats}
        for s in self.unlocked:
            gains[s] += max(1, self.stats[s] * 0.05)

        for i, lower in enumerate(self.unlocked):
            for j in range(i+1, len(self.unlocked)):
                higher = self.unlocked[j]
                distance = j - i
                h_val = self.stats[higher]

                if 1 <= distance <= 5:
                    gains[lower] += h_val * (5 * distance) * self.all_boost
                else:
                    exp = distance - 5
                    if exp > 10:
                        exp = 10 + math.log10(exp)
                    gains[lower] += h_val * (self.stats[lower] ** exp) * self.all_boost

        for s in self.stats:
            self.stats[s] += gains[s]

        self.stats["a"] *= 3 * self.a_boost
        return self.stats["a"]

    def buy_upgrade(self):
        if self.stats["a"] >= self.upgrade_price:
            self.stats["a"] -= self.upgrade_price
            self.all_boost *= 2
            self.upgrade_price *= 10
            return "✅ Upgrade bought! All boosts ×2."
        return "❌ Not enough 'a'!"

    def unlock_next(self):
        if self.stats["a"] >= self.unlock_cost:
            self.stats["a"] -= self.unlock_cost
            next_stat = self._next_stat_name(self.unlocked[-1])
            self.unlocked.append(next_stat)
            self.stats[next_stat] = 10.0
            self.unlock_cost *= 10
            return f"🔓 Unlocked new stat: {next_stat} (auto-generating now!)"
        return f"❌ Need {self._format(self.unlock_cost)} a to unlock next stat!"

    def _next_stat_name(self, name):
        alphabet = [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)]
        if name not in alphabet:
            prefix, last = name[:-1], name[-1]
            if last == "Z": return prefix + "a"
            return prefix + alphabet[alphabet.index(last)+1]
        return "aa" if name=="Z" else alphabet[alphabet.index(name)+1]

    def start_challenge(self):
        if self.challenge_active:
            return "⚠️ Already in a challenge!"
        self.challenge_active = True
        self.challenge_level += 1
        self._reset_progress()
        return f"🏁 Challenge {self.challenge_level} started! Progress reset."

    def complete_challenge(self):
        if not self.challenge_active:
            return "❌ Not in a challenge."
        reward = 1 + (self.challenge_level * 0.5)
        self.a_boost *= reward
        self.challenge_active = False
        return f"🎉 Challenge {self.challenge_level} complete! 'a' boost ×{reward:.2f}"

    def _reset_progress(self):
        self.stats = {"a": 10.0}
        self.unlocked = ["a"]
        self.all_boost = 1
        self.a_boost = 1
        self.upgrade_price = 100
        self.unlock_cost = 100

    def _format(self, n):
        suffixes = ["","K","M","B","T","Qd","Qn","Sx","Sp","Oc","No","De"]
        if n < 1000: return f"{n:.2f}"
        exp = int(math.log10(n)//3)
        exp = min(exp, len(suffixes)-1)
        return f"{n/(10**(3*exp)):.2f}{suffixes[exp]}"

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Incremental Stats Game v3 🧮")
        self.root.geometry("420x420")
        self.root.resizable(False, False)
        self.game = Game()

        # Info panel
        self.info = tk.Label(root, text="", justify="left", font=("Consolas", 11))
        self.info.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Tick", command=self.tick).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Upgrade", command=self.upgrade).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Unlock", command=self.unlock).grid(row=_
