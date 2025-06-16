import time
import sys

# Typing effect function (with the help of ChatGPT)
def type_text(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Function to get a user input within a range and re-ask if input is wrong/impossible
def get_user_input(user_input, min_val, max_val):
    while True:
        val = input(user_input)
        if val.isdigit():  # Check if input is a valid number (help of ChatGPT)
            val = int(val)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        else:
            print("Hmm something went wrong... Please enter a valid number!")



type_text("Welcome to the Vibe Checker", 0.05)
time.sleep(1)

# Collecting user inputs
name = input("What’s your name? ")
age = get_user_input("How old are you? Please enter your age. ", 0, 150)
yesterday = input("How was your day yesterday? Please type Good/Bad/Okay: ").strip().lower()

# Here I ask for weather and sleep infos
weather = get_user_input("On a scale from 1 to 10, how nice is the weather today?: ", 1, 10)
sleep = get_user_input("How many hours of sleep did you get last night?: ", 0, 24)

type_text(f"\nAight, {name}... Let me calculate today's vibe...", 0.05)
time.sleep(1)

# Personalized responses based on inputs
if weather >= 8 and sleep >= 7:
    type_text(f"You’re in great form, {name}! The weather’s perfect and you had a solid sleep! You're killing it today!")
elif weather < 5 and sleep < 6:
    type_text(f"Hey, {name}, looks like yesterday drained you. The weather’s not helping either. But hey, you're still slaying!")
elif weather >= 7 and sleep < 6:
    type_text(f"The weather’s looking good, {name}, but you're running low on sleep. Go get that double espresso to power through!")
elif weather < 5 and sleep >= 7:
    type_text(f"It's gloomy outside, but you got your rest, {name}. You can still chill inside though!")
elif 5 <= weather <= 7 and 6 <= sleep <= 8:
    type_text(f"Kinda mid, huh, {name}? I guess it's gonna be a normal day, you'll make it work!")
else:
    type_text(f"It’s a weird mix today, {name}. Can't really get your vibes but hey who cares, go seize the day!")

# Comment based on how yesterday went
if yesterday == "good":
    type_text(f"\n And glad to hear you had a great day yesterday! Try to carry that positive energy with you today!")
elif yesterday == "bad":
    type_text(f"\nToo bad it was a tough day yesterday, {name}. But hey, today is a new chance to turn things around!")
elif yesterday == "okay":
    type_text(f"\nAnd yesterday was an okay day, huh? Well, today can be whatever you make it!")

# End message
type_text(f"\nThat was your vibe check! Make sure to swing by again tomorrow!")
