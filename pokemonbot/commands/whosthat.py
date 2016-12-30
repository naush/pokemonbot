import random

from pokemonbot.database.interface import load, save

COMMAND = "who’s that pokemon"

def respond(user_id, user_input):
    data = load('pokemonbot/database/pokemons.json')
    pokemon_names = [pokemon['name'] for pokemon in data['pokemons']]
    users = load('pokemonbot/database/users.json')

    if user_id in users:
        user_data = users[user_id]
    else:
        user_data = {}

    if 'context' in user_data:
        pokemon = user_data['context']['pokemon']
        if pokemon in user_input:
            response = 'You got it!'
            user_data = {}
        else:
            attempt = user_data['context']['attempt'] + 1
            user_data['context']['attempt'] = attempt

            if attempt < 3:
                response = 'Nope.'
            elif attempt < 4:
                response = 'Are you even a Pokémon fan?'
            elif attempt < 5:
                response = 'Last chance.'
            else:
                response = 'It’s a ' + pokemon + '. Go read a Pokédex.'
                user_data = {}
    else:
        pokemon = random.choice(pokemon_names)
        user_data['context'] = {'pokemon':pokemon, 'attempt':0}
        user_data['command'] = COMMAND
        response = 'Who is that pokemon? :pokemon-' + pokemon + ':'

    users[user_id] = user_data
    save(users)

    return response
