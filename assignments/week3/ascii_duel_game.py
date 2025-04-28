# My wizard game kinda missed the point of the assignment
# but I was too invested in it already oops
# anyways I hope you enjoy the duel!

import random
import time

# different spell effects with different shapes based on the spell power
spell_effects = {
    "light": ["✨", "✨✨", "✨✨✨", "✨✨✨✨", "✨✨✨✨✨"],  # Light Magic
    "fire": ["🔥", "🔥🔥", "🔥🔥🔥", "🔥🔥🔥🔥", "🔥🔥🔥🔥🔥"],  # Fire Magic
    "wind": ["💨", "💨💨", "💨💨💨", "💨💨💨💨", "💨💨💨💨💨"],  # Wind Magic
    "ice": ["❄️", "❄️❄️", "❄️❄️❄️", "❄️❄️❄️❄️", "❄️❄️❄️❄️❄️"],  # Ice Magic
}

# Wizard ASCII Art
wizard_ascii = """
         ,/   *
      _,'/_   |
      `(")' ,'/
   _ _,-H-./ /
   \_\_\.   /
     )" |  (
  __/   H  \ __
  \    /|\    /
   `--'|||`--'
      ==^==
"""

# Attack ASCII Art
attack_ascii = """
⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⢹⣿⡟⠻⠿⢶⣶⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣿⡟⠀⠀⠀⢀⣤⣤⣈⠉⠙⠛⠛⠻⠿⠶⣶⣤⣤⣤⣀⣀
⣾⣿⡃⠀⠀⢠⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛
⠙⢿⣿⣦⡀⠀⠻⣿⣿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⢿⣿⣶⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⣀⣀⣀⣀⣤⡀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⡟⠻⠿⠿⠿⠿⠿⠿⠛⠛⠁⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣾⣿⣿⣿⠿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⣿⣿⠟⠁⠀⠈⠻⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⡏⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣷⡄⠀⠀⠀⠀⠀⠀
⠀⢸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣦⠀⠀⠀⠀⠀
⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀
"""

# Defend ASCII Art
defend_ascii = """
    |`-._/\_.-`|
    |    ||    |
    |___o()o___|
    |__((<>))__|
    \   o\/o   /
     \   ||   /
      \  ||  /
       '.||.'
"""

# Function to not get wrong input
def user_input(prompt, min_val, max_val):
    while True:
        try:
            num = int(input(prompt))
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Please enter a number between {min_val} and {max_val}!")
        except ValueError:
            print("That's not a valid number. Try again!")

# Function to create the spell effect based on spell power
def create_spell_effect(spell_type, spell_power, magic_word):
    spell_shape = random.choice(spell_effects[spell_type])

# Function to create the wand with the spell effect at the tip
def create_wand_with_effect(spell_type):
    spell_tip = ""
    if spell_type == "light":
        spell_tip = "✨"
    elif spell_type == "fire":
        spell_tip = "🔥"
    elif spell_type == "wind":
        spell_tip = "💨"
    elif spell_type == "ice":
        spell_tip = "❄️"

    # Replace '*' in the wizard ASCII with the spell tip
    updated_wizard = wizard_ascii.replace('*', spell_tip)

    return updated_wizard

# Function to display HP as hearts
def display_hp(current_hp):
    max_hearts = 10
    hp_per_heart = 3
    full_hearts = current_hp // hp_per_heart
    empty_hearts = max_hearts - full_hearts
    return ("♥" * full_hearts) + ("♡" * empty_hearts)

# Get user inputs
print("Welcome to Duel Against Jan Müggenburg!\n")

explanation = [
    "In this duel, you face off against Jan Müggenburg using spells.",
    "You choose to attack or defend each round.",
    "Spells deal random damage, with a 40% chance for a Critical Hit.",
    "The first to reduce the other's HP to 0 wins the duel.",
    "The game ends after 3 rounds."
]

for line in explanation:
    print(line)
    time.sleep(2)

wizard = input("Enter the name for your Wizard: ").strip() or "Wizard"
spell_type = input("Choose your spell type (light, fire, wind, ice): ").strip().lower()
spell_power = user_input("Enter your spell power (1-5): ", 1, 5)
num_rounds = 3
magic_word = input("Enter your magic word (Example: AHHHHHH!): ")

# Set starting HP
hp_a = 30
hp_b = 30

# Start Duel
print(f"\n✨ The Duel between {wizard} and Jan Müggenburg begins! ✨\n")
time.sleep(1)

# Duel rounds
for round_num in range(1, num_rounds + 1):
    print(f"\n--- Round {round_num} ---")

    # Display the wizard ASCII at the start of each round, now with the wand effect!
    print(create_wand_with_effect(spell_type))
    time.sleep(0.5)

    action = input(f"{wizard}, choose your action (attack/defend): ").strip().lower()
    if action not in ['attack', 'defend']:
        print("Invalid action, defaulting to attack!")
        action = 'attack'

    if action == 'attack':
        print(attack_ascii)
    else:
        print(defend_ascii)

    spell_effect = create_spell_effect(spell_type, spell_power, magic_word)

    print(f"\n{wizard} shouts: {magic_word.upper()} ")
    time.sleep(0.5)

    print(spell_effect)
    time.sleep(1)

    funny_comments = [
        "That had to hurt!",
        "Ouch, what a hit!",
        "That spell was nasty!",
        "Boom! Right where it hurt!",
        "A direct hit to the pointy hat!"
    ]
    print(random.choice(funny_comments))

    # Damage calculation
    damage = random.randint(2, 4)
    critical_hit = random.random() < 0.4  # 40% chance
    if critical_hit:
        print("💥 CRITICAL HIT! 💥")
        damage *= 2

    if action == 'attack':
        hp_b -= damage
        print(f"{wizard} deals {damage} damage to Jan Müggenburg!")
    else: # I had ChatGPT help me here
        hp_a -= max(1, damage // 2)
        print(f"{wizard} blocks but still takes {max(1, damage // 2)} damage!")

    hp_a = max(hp_a, 0)
    hp_b = max(hp_b, 0)

    print("\nCurrent HP:")
    print(f"{wizard}: {display_hp(hp_a)} ({hp_a}/30)")
    print(f"Jan Müggenburg: {display_hp(hp_b)} ({hp_b}/30)")

    # Allow the user to change the spell type after each round
    spell_type = input(f"Choose your spell type for next round (light, fire, wind, ice): ").strip().lower()

    if spell_type not in spell_effects:
        print("Invalid spell type! Defaulting to 'light'.")
        spell_type = "light"

    if hp_a <= 0 or hp_b <= 0:
        break
    time.sleep(1)

# Final Results
print("\n🏆 Final Duel Results 🏆")
print(f"{wizard}: {display_hp(hp_a)} ({hp_a}/30)")
print(f"Jan Müggenburg: {display_hp(hp_b)} ({hp_b}/30)")

if hp_a > hp_b:
    print(f"\n✨ {wizard} is the Grand Wizard Champion! ✨")
elif hp_b > hp_a:
    print(f"\n✨ Jan Müggenburg is the Grand Wizard Champion! ✨")
else:
    print("\n⚡ It's a Tie! Both you and Jan collapse at the same time! ⚡")
