import json
import time
import random

from groupmebot import GroupMeBot


# Loads config file, which contains the BOT_ID and Minecraft Server IP for
# /mcserver command
with open('config.json', 'r') as f:
    config = json.load(f)

bot = GroupMeBot(config['BOT_ID'])

# A couple commands use random, so set a seed here
random.seed(time.time())


"""
Minecraft Server Status:
    /mcserver - Minecraft Server Status
"""
from mcstatus import MinecraftServer

@bot.command("/mcserver")
def mcserver(args):
    """
    Uses mcstatus to query the server and respond with the online players
    """

    # Loads the IP for config file, var is MC_SERVER
    mcserver = MinecraftServer.lookup(config['MC_SERVER'])
    query = mcserver.query()

    # Sassy responses when no one is on
    if query.players.online == 0:
        responses = [
            "No one is playing :(",
            "No one is on!",
            "Nope! No one is here :/",
            "It's empty",
            "Were you looking for friends? There are no friends here.",
            "Why would you think people are playing.",
            "No one. Please play on me :(",
            "No"
        ]
        response_text = random.choice(responses)

    # Handle response for one player
    if query.players.online == 1:
        response_text = "{} is playing!".format(query.players.names[0])

    # Format response as player 1, player 2, ... and player N are playing
    if query.players.online >= 2:
        response_text = "{} and {} are playing!".format(
            ", ".join(query.players.names[:-1]),
            query.players.names[-1]
        )

    bot.post(response_text)


"""
GIF Command:
    /gif <phrase> - Search GIPHY for phrase
"""
from giphypop import translate

@bot.command("/gif")
def gif(args):
    """
    Uses GIPHY API and 'translates' the phrase to a gif
    """

    # combine args in single phrase and search giphy
    img = translate(phrase=" ".join(args))

    if img:
        bot.post(img.fixed_height.url)


"""
Magic 8-ball command:
    /m8 <question> - Ask Magic 8-ball a question
"""

@bot.command("/m8")
def m8(args):
    """
    Magic 8-ball, randomly choose a response
    """

    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes, definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    response_text = random.choice(responses)
    bot.post(response_text)


"""
Roll command:
    /roll <number> - Roll a dice. Defaults to 6-sided
"""
@bot.command("/roll")
def roll(args):
    """
    Roll a dice, inspired by Google Hangouts. Optional argument to specify how
    many sides.
    """

    dice = 6

    # Attempt to parse if any arguments
    if args:
        try:
            dice = int(args[0])
        except Exception:
            dice = 6

    response_text = "You rolled a %d" % random.randint(1, dice)
    bot.post(response_text)


"""
Help Command:
    /help - Show this help thing
"""
@bot.command("/help")
def help(args):
    """
    Responds with a list of commands
    """

    # List of commands. Joined by a newline and then posted
    commands = [
        "/mcserver - Minecraft Server Status",
        "/gif <phrase> - Search GIPHY for phrase",
        "/m8 <question> - Ask Magic 8-ball a question",
        "/roll <number> - Roll a dice. Defaults to 6-sided",
        "/help - Show this help thing"
    ]
    bot.post("\n".join(commands))


if __name__ == "__main__":
    # Serve forever
    bot.serve(debug=True, host='0.0.0.0', port=4000, threaded=True)
