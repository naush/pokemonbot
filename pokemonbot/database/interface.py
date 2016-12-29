import json

def load(filename):
    with open(filename) as data_file:
        return json.load(data_file)

def save(data):
    with open('pokemonbot/database/users.json', 'w') as data_file:
        json.dump(data, data_file)
