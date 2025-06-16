import pyjokes
import cowsay
from playsound import playsound
from randomizer import random_character, type_colored

type_colored("Here comes a hilarious joke...")

random_character(pyjokes.get_joke())
playsound("laugh.mp3")







