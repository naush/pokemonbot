from pokemonbot.commands import whois, whosthat
from pokemonbot.database.interface import load

def listen(user_id, user_name, user_input):
    users = load('pokemonbot/database/users.json')
    response = "Say *who is* " + user_name + " or *who’s that pokemon* to start a game."

    if user_id in users:
        user_data = users[user_id]
    else:
        user_data = {}

    if 'command' in user_data: # TODO: Track state in addition to command
        command = user_data['command']
        if command == whosthat.COMMAND:
            response = whosthat.respond(user_id, user_input)
    elif user_input.startswith(whois.COMMAND):
        response = whois.respond(user_name, user_input)
    elif user_input.startswith(whosthat.COMMAND):
        response = whosthat.respond(user_id, user_input)

    return response
