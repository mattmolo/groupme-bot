import json
import time
import random

from groupmebot import GroupmeBot

random.seed(time.time())


with open('config.json', 'r') as f:
    config = json.load(f)

bot = GroupmeBot(config['BOT_ID_DEV'])


"""
Minecraft Server Status:
    /mcserver
    Responds with the players currently online
"""
from mcstatus import MinecraftServer

@bot.command("/mcserver")
def mcserver(args):

    mcserver = MinecraftServer.lookup(config['MC_SERVER'])
    query = mcserver.query()

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
    /gif <phrase>
    Searches giphy for phrase
"""
from giphypop import translate

@bot.command("/gif")
def gif(args):

    # combine args in single phrase and search giphy
    img = translate(phrase=" ".join(args))

    if img:
        bot.post(img.fixed_height.url)
        bot.post("Powered by GIPHY")


"""
Magic 8-ball command:
    /m8 <phrase>
    responds like a magic 8-ball
"""

@bot.command("/m8")
def m8(args):
    responses = [
        "it is certain.",
        "it is decidedly so.",
        "without a doubt.",
        "yes, definitely.",
        "you may rely on it.",
        "as i see it, yes.",
        "most likely.",
        "outlook good.",
        "yes.",
        "signs point to yes.",
        "reply hazy try again.",
        "ask again later.",
        "better not tell you now.",
        "cannot predict now.",
        "concentrate and ask again.",
        "don't count on it.",
        "my reply is no.",
        "my sources say no.",
        "outlook not so good.",
        "very doubtful."
    ]
    response_text = random.choice(responses)
    bot.post(response_text)


"""
Roll command:
    /roll <number>
    Roll a dice. Defaults to 6-sided
"""
@bot.command("/roll")
def roll(args):

    dice = 6

    if args:
        try:
            dice = int(args[0])
        except Exception:
            dice = 6

    response_text = "You rolled a {}".format(random.randint(1, dice))
    bot.post(response_text)


"""
Help Command:
    /help
    Responds with list of commands
"""
@bot.command("/help")
def help(args):
    commands = [
        "/mcstatus - Minecraft Server Status",
        "/gif <phrase> - Search GIPHY for phrase",
        "/m8 <question> - Ask Magic 8-ball a question",
        "/roll <number> - Roll a dice. Defaults to 6-sided",
        "/help - Show this help thing"
    ]
    bot.post("\n".join(commands))


if __name__ == "__main__":
    # Serve forever
    bot.serve(debug=True, host='0.0.0.0', port=4000, threaded=True)
