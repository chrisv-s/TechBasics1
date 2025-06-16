import cowsay
import random
import sys
import time
from colorama import Back

characters = [
    cowsay.cow,
    cowsay.tux,
    cowsay.dragon,
    cowsay.trex,
    cowsay.beavis,
    cowsay.stegosaurus
]

def random_character(message):
    random.choice(characters)(message)

def type_colored(text, color=Back.GREEN, speed=0.05):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

