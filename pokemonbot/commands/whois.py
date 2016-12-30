import random
import re

from pokemonbot.database.interface import load, save

COMMAND = "who is"

def respond(user_name, user_input):
    data = load('pokemonbot/database/pokemons.json')
    pokemon_names = [pokemon['name'] for pokemon in data['pokemons']]
    subject = user_input.split(COMMAND)[1]
    return re.sub(r'\W+', '', subject) + " is a :pokemon-" + random.choice(pokemon_names) + ":."
