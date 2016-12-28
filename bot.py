import os
import time
import json

from slackclient import SlackClient
from pokemonbot.commands import whois, whosthat

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(BOT_TOKEN)

def load():
    with open('data.json') as data_file:
        return json.load(data_file)

def save(data):
    with open('data.json', 'w') as data_file:
        json.dump(data, data_file)

def handle_command(user, command, channel):
    user_name = user.get('name')
    user_id = user.get('id')
    data = load()

    response = "Say *who is* " + user_name + " or *who’s that pokemon* to start a game."

    if user_id in data:
        user_data = data[user_id]
    else:
        user_data = {}

    if 'command' in user_data:
        if command == 'yes':
            response = 'Phew! That was a tough one.'
            question_no = len(user_data['context'])
            user_data['context'][question_no - 1]['answer'] = command
            print(user_data) # TODO: store user data for future reference
            data[user_id] = {}
            save(data)
        else:
            response = whosthat.respond(user_data, command)
            question_no = len(user_data['context'])
            user_data['context'][question_no - 1]['answer'] = command
            user_data['context'].append({'question':response})
            data[user_id] = user_data
            save(data)
    elif command.startswith(whois.COMMAND):
        response = whois.respond(user_name, command)
    elif command.startswith(whosthat.COMMAND):
        response = whosthat.respond(user_data, command)
        user_data['command'] = whosthat.COMMAND
        user_data['context'] = [{'question':response}]
        data[user_id] = user_data
        save(data)

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
                user_id, command, channel = parse_slack_output(slack_client.rtm_read())
                if user_id and command and channel:
                    for user in users:
                        if 'id' in user and user.get('id') == user_id:
                            handle_command(user, command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
