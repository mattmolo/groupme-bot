import requests
from flask import Flask, request

class GroupmeBot():
    def __init__(self, bot_id):
        self._bot_id = bot_id
        self._commands = {}
        self._flask = Flask("GroupmeBot")

        @self._flask.route('/', methods=['GET', 'POST'])
        def _callback():

            # Don't reply to bots
            if request.get_json()['sender_type'] == 'bot':
                return ''

            message_text = request.get_json()['text']

            if message_text[0] == '/':

                message_text = message_text.replace(u'\xa0', ' ')
                split_message = message_text.split()

                command = split_message[0]
                command_function = self._commands.get(command)

                if command_function:
                    command_args = []
                    if len(split_message) > 1:
                        command_args = split_message[1:]

                    command_function(command_args)

            return ''

    def command(self, command_str):
        def decorator(f):
            self._commands[command_str] = f
            return f

        return decorator

    def serve(self, *args, **kwargs):
        self._flask.run(*args, **kwargs)

    def post(self, message):
        response = {
            "bot_id": self._bot_id,
            "text": message
        }
        requests.post("https://api.groupme.com/v3/bots/post", data=response)
