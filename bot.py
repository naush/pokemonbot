import os
import time

from slackclient import SlackClient
from pokemonbot.commands import whois, whosthat
from pokemonbot.database.interface import load

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(BOT_TOKEN)

def handle_user_input(user, user_input, channel):
    user_name = user.get('name')
    user_id = user.get('id')
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

    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['user'], output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            print("PokemonBot connected and running!")
            while True:
                user_id, user_input, channel = parse_slack_output(slack_client.rtm_read())
                if user_id and user_input and channel:
                    for user in users:
                        if 'id' in user and user.get('id') == user_id:
                            handle_user_input(user, user_input.lower(), channel)
                time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
