# GroupMe Bot
A simple GroupMe Bot that starts a HTTP server to handle the bot callbacks. The [GroupMe dev site](https://dev.groupme.com/bots) allows you to create a bot and set your callback.

The GroupMe bot class is made similar to flask, so you can define your commands with decorators. Check the example for an in depth version.

## Examples
### Simple Bot
```python
from groupmebot import GroupMeBot

BOT_ID = "" # Get from GroupMe dev site
bot = GroupMeBot(BOT_ID)

@bot.command("/hello")
def hellothere(args):
    bot.post("Hello there!")


if __name__ == "__main__":
    # Serve forever
    bot.serve(host='0.0.0.0', port=4000, threaded=True)
```

### Arguments
Commands can also access text (arguments) after the command. They are split on whitespace and passed in as a list:
```python
@bot.command("/mynameis")
def mynameis(args):
    if args:
        bot.post("Hello, %s!" % args[0])
```

## GroupMeBot API Reference:
`GroupMeBot(bot_id: string)`: Initializes the bot. `bot_id` is needed to post a message to the GroupMe.

`command(command_str: string)`: Used to decorate functions that are called when the first word of the text matches `command_str`. The decorated function is passed a list of arguments when the command was called.

`post(message: string)`: Post a message to your GroupMe. The GroupMe is defined by the `bot_id` when initialized.

`serve(*args, **kwargs)`: Starts the server and listens for callbacks. The arguments are actually passed to [Flask's run command](http://flask.pocoo.org/docs/0.12/api/#flask.Flask.run). As per Flask's documentation, it is not the recommended way to run the server, but is useful for debugging. Look into [Flask's deployment options](http://flask.pocoo.org/docs/0.12/deploying/#deployment) for production use. (Though, I find this good enough for a GroupMe that isn't averaging 100/requests(messages)/second like a real web server)
