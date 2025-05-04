# My game checks your daily "vibe" based on sleep, weather, how yesterday went, and age, giving a custom message and score.

import time
import sys

# Some constants I define that I can play with later
text_delay = 0.05
min_age = 0
max_age = 120
min_weather = 1
max_weather = 10
min_sleep = 0
max_sleep = 24
mood_multiplier = 0.9

# function 1: print text with typing animation
def type_text(text, delay=text_delay):
    for characters in text:
        sys.stdout.write(characters)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# function 2: get a valid input from the user (basically convert the input into an integer I can work with)
def get_valid_input(user_input, min_val, max_val):
    while True:
        val = input(user_input)
        if val.isdigit():
            val = int(val)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Hmm, please enter a number between {min_val} and {max_val}.")
        else:
            print(f"Hmm, please enter a valid number.")

# function 3: custom messages based on weather and sleep quality
def analyze_vibe(name, weather_score, sleep_hours): # I use the parameters weather_score and sleep_hours for better readability
    if weather_score >= 8 and sleep_hours >= 7:
        return f"\nYou’re in great form, {name}! The weather’s perfect and you had a solid sleep! You're killing it today!"
    elif weather_score < 5 and sleep_hours < 6:
        return f"\nHey, {name}, looks like yesterday drained you. The weather’s not helping either. But hey, you're still slaying!"
    elif weather_score >= 7 and sleep_hours < 6:
        return f"\nThe weather’s looking good, {name}, but you're running low on sleep. Go get that double espresso to power through!"
    elif weather_score < 5 and sleep_hours >= 7:
        return f"\nIt's gloomy outside, but you got your rest, {name}. You can still chill inside though!"
    elif 5 <= weather_score <= 7 and 6 <= sleep_hours <= 8:
        return f"\nKinda mid, huh, {name}? I guess it's gonna be a normal day, you'll make it work!"
    else:
        return f"\nIt’s a weird mix today, {name}. Can't really get your vibes but hey who cares, go seize the day!"

# function 4: I added this function in this new version of the game to play around more with the given user inputs and to use the global value of mood_multiplier
def calculate_vibe_score(weather_score, sleep_hours, yesterday, age):
    weather_effect = weather_score * mood_multiplier
    sleep_effect = sleep_hours * mood_multiplier

    mood_bonus = {
        "good": 2,
        "okay": 1,
        "bad": -2
    }.get(yesterday, 0) # get score based on user input and if input isn't in the dictionary, it defaults to 0

    if age < 30:
        age_bonus = 1
    elif age > 60:
        age_bonus = -1
    else:
        age_bonus = 0

    score = (weather_effect + sleep_effect) / 2 + mood_bonus + age_bonus
    print(f"Calculated Score (before rounding): {score}")  # Debugging line to check the score
    return round(min(score, 10), 1)

# function 5: message based on user's feedback about yesterday
def how_was_yesterday(feedback, name):
    if feedback == "good":
        return f"\nGlad to hear you had a great day yesterday! Try to carry that positive energy with you today!"
    elif feedback == "bad":
        return f"\nToo bad it was a tough day yesterday, {name}. But hey, today is a new chance to turn things around!"
    elif feedback == "okay":
        return f"\nYesterday was an okay day, huh? Well, today can be whatever you make it!"
    else:
        return f"\nWell, vibes are vibes – let’s just keep moving!"

# main game flow
def main():
    type_text("Welcome to the Vibe Checker!")

    # now I collect user inputs
    name = input("What's your name?")
    age = get_valid_input("How old are you? Please enter your age: ", min_age, max_age)
    yesterday = input("How was your day yesterday? Please type Good/Bad/Okay: ").strip().lower()

    yesterday_comment = how_was_yesterday(yesterday, name)
    type_text(yesterday_comment)

    weather = get_valid_input(f"\nOn a scale from 1 to 10, how nice is the weather today?: ", min_weather, max_weather)
    sleep = get_valid_input("How many hours of sleep did you get last night?: ", min_sleep, max_sleep)

    type_text(f"\nAight, {name}... Let me calculate today's vibe...")
    time.sleep(1)

    vibe_results = analyze_vibe(name, weather, sleep)
    type_text(vibe_results)

    vibe_score = calculate_vibe_score(weather, sleep, yesterday, age)
    type_text(f"\nYour vibe score for today is: {vibe_score}/10 ")

    type_text(f"\nThat was your vibe check! Make sure to swing by again tomorrow!")

if __name__ == "__main__":
    main()
