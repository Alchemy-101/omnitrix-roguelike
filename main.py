from dataclasses import dataclass, asdict
import json
import random

SAVE_FILE = "save.json"

# -------------------- Models --------------------

@dataclass
class Alien:
    key: str
    name: str
    max_hp: int
    atk: int
    defense: int
    ability_name: str

@dataclass
class Player:
    dna: int
    unlocked: list
    omnitrix_energy_max: int = 3

@dataclass
class RunState:
    current_alien: Alien
    hp: int
    omnitrix_energy: int
    rooms_cleared: int = 0
    dna_earned: int = 0

@dataclass
class Enemy:
    name: str
    hp: int
    atk: int


ALIENS = {
    "bruiser": Alien("bruiser", "Bruiser Form", 120, 15, 8, "Power Smash"),
    "pyro": Alien("pyro", "Pyro Form", 85, 20, 4, "Fire Burst"),
    "speed": Alien("speed", "Speed Form", 75, 14, 3, "Quick Step"),
    "crystal": Alien("crystal", "Crystal Form", 100, 16, 10, "Shield Wall"),
}

# -------------------- Save System --------------------

def load_player():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return Player(data["dna"], data["unlocked"], data["omnitrix_energy_max"])
    except:
        return Player(0, ["bruiser", "pyro"], 3)

def save_player(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(asdict(player), f, indent=2)

# -------------------- Helper --------------------

def choose(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    while True:
        choice = input("Choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        print("Invalid choice.")

# -------------------- Combat --------------------

def damage(atk, defense):
    return max(1, atk - defense // 2)

def combat(run):
    enemy = Enemy("Drone Bot", 50 + run.rooms_cleared * 10, 10 + run.rooms_cleared * 2)
    ability_cd = 0
    burn = 0

    print("\n=== COMBAT ROOM ===")
    print(f"Enemy: {enemy.name} | HP: {enemy.hp}")

    while run.hp > 0 and enemy.hp > 0:

        if burn > 0:
            enemy.hp -= 5
            burn -= 1
            print("Burn deals 5 damage.")

        print(f"\nYou are {run.current_alien.name}")
        print(f"Your HP: {run.hp}")
        print(f"Enemy HP: {enemy.hp}")
        print(f"Omnitrix Energy: {run.omnitrix_energy}")

        choice = choose("Choose action:", [
            "Basic Attack",
            f"Use Ability ({ability_cd} turn cooldown)",
            "Transform"
        ])

        if choice == 0:
            dealt = damage(run.current_alien.atk, 0)
            enemy.hp -= dealt
            print(f"You deal {dealt} damage.")

        elif choice == 1:
            if ability_cd > 0:
                print("Ability on cooldown.")
            else:
                if run.current_alien.key == "bruiser":
                    dealt = damage(run.current_alien.atk * 2, 0)
                    enemy.hp -= dealt
                    print("Power Smash!")
                elif run.current_alien.key == "pyro":
                    dealt = damage(run.current_alien.atk + 5, 0)
                    enemy.hp -= dealt
                    burn = 3
                    print("Fire Burst! Burn applied.")
                else:
                    dealt = damage(run.current_alien.atk + 3, 0)
                    enemy.hp -= dealt
                ability_cd = 2

        else:
            if run.omnitrix_energy > 0:
                unlocked = [ALIENS[k] for k in player.unlocked]
                idx = choose("Transform into:", [a.name for a in unlocked])
                run.current_alien = unlocked[idx]
                run.hp = min(run.hp, run.current_alien.max_hp)
                run.omnitrix_energy -= 1
                print("Transformed.")
            else:
                print("No energy left.")

        if ability_cd > 0:
            ability_cd -= 1

        if enemy.hp > 0:
            taken = damage(enemy.atk, run.current_alien.defense)
            run.hp -= taken
            print(f"Enemy hits for {taken} damage.")

    if run.hp > 0:
        earned = 10
        run.dna_earned += earned
        run.rooms_cleared += 1
        print(f"\nVictory! +{earned} DNA")
        return True
    else:
        print("\nYou were defeated.")
        return False

# -------------------- Rooms --------------------

def run_game(player):
    unlocked = [ALIENS[k] for k in player.unlocked]
    idx = choose("Choose starting alien:", [a.name for a in unlocked])
    start = unlocked[idx]

    run = RunState(start, start.max_hp, player.omnitrix_energy_max)

    for i in range(5):
        if not combat(run):
            break

    print("\n=== RUN OVER ===")
    print(f"Rooms cleared: {run.rooms_cleared}")
    print(f"DNA earned: {run.dna_earned}")

    player.dna += run.dna_earned
    save_player(player)

# -------------------- DNA Lab --------------------

def dna_lab(player):
    print(f"\nDNA Available: {player.dna}")

    options = [
        "Unlock Speed Form (30 DNA)",
        "Unlock Crystal Form (40 DNA)",
        "Exit"
    ]

    choice = choose("DNA Lab:", options)

    if choice == 0 and "speed" not in player.unlocked and player.dna >= 30:
        player.unlocked.append("speed")
        player.dna -= 30
        print("Speed Form unlocked.")
    elif choice == 1 and "crystal" not in player.unlocked and player.dna >= 40:
        player.unlocked.append("crystal")
        player.dna -= 40
        print("Crystal Form unlocked.")
    save_player(player)

# -------------------- Main Loop --------------------

player = load_player()

while True:
    print("\n=== OMNITRIX ROGUELIKE ===")
    print(f"DNA: {player.dna}")

    choice = choose("Menu:", ["Start Run", "DNA Lab", "Quit"])

    if choice == 0:
        run_game(player)
    elif choice == 1:
        dna_lab(player)
    else:
        break
