#!/usr/bin/env python3
# Incremental Stats Game v2 🧮
# Auto-gaining system with working stat generation and boosts

import math, random

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

    # Each tick: every stat generates its own value and boosts lower stats
    def tick(self):
        gains = {k: 0 for k in self.stats}

        # Each stat grows on its own
        for s in self.unlocked:
            gains[s] += max(1, self.stats[s] * 0.05)  # base growth per tick

        # Boosting logic (higher stats boost lower ones)
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

        # Apply gains
        for s in self.stats:
            self.stats[s] += gains[s]

        # “a” triples per tick (your rule)
        self.stats["a"] *= 3 * self.a_boost

        return self.stats["a"]

    def buy_upgrade(self):
        if self.stats["a"] >= self.upgrade_price:
            self.stats["a"] -= self.upgrade_price
            self.all_boost *= 2
            self.upgrade_price *= 10
            print("✅ Upgrade bought! All boosts ×2.")
        else:
            print("❌ Not enough 'a'!")

    def unlock_next(self):
        if self.stats["a"] >= self.unlock_cost:
            self.stats["a"] -= self.unlock_cost
            next_stat = self._next_stat_name(self.unlocked[-1])
            self.unlocked.append(next_stat)
            self.stats[next_stat] = 10.0  # start generating immediately
            self.unlock_cost *= 10
            print(f"🔓 Unlocked new stat: {next_stat} (auto-generating now!)")
        else:
            print(f"❌ Need {self._format(self.unlock_cost)} a to unlock next stat!")

    def _next_stat_name(self, name):
        alphabet = [chr(i) for i in range(97,123)] + [chr(i) for i in range(65,91)]
        if name not in alphabet:
            prefix, last = name[:-1], name[-1]
            if last == "Z":
                return prefix + "a"
            return prefix + alphabet[alphabet.index(last)+1]
        return "aa" if name=="Z" else alphabet[alphabet.index(name)+1]

    def start_challenge(self):
        if self.challenge_active:
            print("⚠️ Already in a challenge!")
            return
        self.challenge_active = True
        self.challenge_level += 1
        self._reset_progress()
        print(f"🏁 Challenge {self.challenge_level} started! Progress reset.")

    def complete_challenge(self):
        if not self.challenge_active:
            print("❌ Not in a challenge.")
            return
        reward = 1 + (self.challenge_level * 0.5)
        self.a_boost *= reward
        self.challenge_active = False
        print(f"🎉 Challenge {self.challenge_level} complete! 'a' boost ×{reward:.2f}")

    def _reset_progress(self):
        self.stats = {"a": 10.0}
        self.unlocked = ["a"]
        self.all_boost = 1
        self.a_boost = 1
        self.upgrade_price = 100
        self.unlock_cost = 100

    def show(self):
        print("\n📊 --- STATUS ---")
        for s in self.unlocked:
            print(f"{s}: {self._format(self.stats[s])}")
        print(f"Unlocked: {self.unlocked}")
        print(f"All boost: ×{self.all_boost}")
        print(f"A boost: ×{self.a_boost}")
        print(f"Upgrade cost: {self._format(self.upgrade_price)} a")
        print(f"Next unlock cost: {self._format(self.unlock_cost)} a")
        print(f"Challenge: {'Active' if self.challenge_active else 'None'} (Level {self.challenge_level})")
        print("-----------------------\n")

    def _format(self, n):
        suffixes = ["","K","M","B","T","Qd","Qn","Sx","Sp","Oc","No","De"]
        if n < 1000: return f"{n:.2f}"
        exp = int(math.log10(n)//3)
        exp = min(exp, len(suffixes)-1)
        return f"{n/(10**(3*exp)):.2f}{suffixes[exp]}"

def main():
    game = Game()
    print("🎮 Welcome to Incremental Stats Game v2!")
    print("Commands: tick / upgrade / unlock / challenge / complete / show / exit")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "tick":
            a = game.tick()
            print(f"Tick... a = {game._format(a)}")
        elif cmd == "upgrade": game.buy_upgrade()
        elif cmd == "unlock": game.unlock_next()
        elif cmd == "challenge": game.start_challenge()
        elif cmd == "complete": game.complete_challenge()
        elif cmd == "show": game.show()
        elif cmd == "exit":
            print("👋 Goodbye!")
            break
        else:
            print("❓ Unknown command!")

if __name__ == "__main__":
    main()
