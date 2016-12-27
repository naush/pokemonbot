import os
import time
from slackclient import SlackClient
from pokemonbot.commands import whois

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(BOT_TOKEN)

def handle_command(user_name, command, channel):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=whois.respond(user_name, command), as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['user'], output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
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
                            handle_command(user.get('name'), command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
