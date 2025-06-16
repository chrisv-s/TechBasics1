import cowsay
import random

characters = [
    cowsay.cow,
    cowsay.tux,
    cowsay.dragon,
    cowsay.trex,
    cowsay.beavis,
    cowsay.stegosaurus
]

def say_random():
    random.choice(characters)(text)