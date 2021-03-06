import sys
import signal
import asyncio
import datetime
from discord.ext import commands
import database_helper
import logging
import random
voice_times = {}
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

COMMANDS_CHANNEL_ID = 282336977418715146
LOGS_CHANNEL_ID = 540189209898647554
DESCRIPTION = '''The senpai of the server.'''

# initialize bot
bot = commands.Bot(command_prefix="!senpai ", description=DESCRIPTION)

def signal_handler(signal, frame):
    '''(Signal, Frame) -> null
    Upon signal, stop the bot and exit the program
    '''

    print("\nLogging out bot...")
    leave_all_voice_channels(bot)
    # log out bot and close connection
    bot.logout()
    bot.close()
    print("Bot has logged out.")
    # exit program
    sys.exit(0)

def leave_all_voice_channels(bot):
    '''(Client) -> null
    makes the Client leave all connected voice channels
    '''

    connected_voices = []
    # get a list of all voice channels the bot is connected to
    for voice in bot.voice_clients:
        # if bot is connected to the channel, add it to the list
        if (voice.is_connected()):
            connected_voices.append(voice)
    # if bot is not connected to any voice channel, print error message
    if (connected_voices):
        # disconnect bot from all connected voice channels
        for voice in connected_voices:
            voice.disconnect()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def leave():
    leave_all_voice_channels(bot)
    print("Left all voice channels")

@bot.event
async def on_voice_state_update(member, before, after):
    if(after.channel != None and member.id not in voice_times):
        voice_times[member.id] = datetime.datetime.now()
    elif(after.channel == None and member.id in voice_times):
        start_time = voice_times[member.id]
        voice_times.pop(member.id)
        channel = bot.get_channel(COMMANDS_CHANNEL_ID)
        elapsed_time = round((datetime.datetime.now()-start_time).total_seconds()/60)
        print(elapsed_time)
        database_helper.add_pikapoints(member.id, elapsed_time)
        if(channel is not None):
            await channel.send("`" + member.display_name + " was in voice channel for " + str(elapsed_time) + " seconds" + "`")
        else:
            pass


@bot.event
async def on_message(message : str):
    try:
        if ":electrocution:" in message.content:
            r = random.randint(1, 420)
            if 1 <= r <= 69:
                await message.channel.send('https://tenor.com/xWBO.gif')
        await bot.process_commands(message)
    except commands.errors.CommandNotFound:
        await bot.say("command not supported")

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(LOGS_CHANNEL_ID)
    msg = ""
    if message.channel.id != LOGS_CHANNEL_ID and message.author != bot.user:
        msg = msg + "`In " + message.channel.name + ", " + message.author.name + " deleted: `" + message.content
        for attachment in message.attachments:
            msg = msg + "\n`proxy url: `" + attachment.proxy_url
        await channel.send(msg)

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(LOGS_CHANNEL_ID)
    msg = ""
    if before.channel.id != LOGS_CHANNEL_ID and before.author != bot.user:
        msg = msg + "`In " + before.channel.name + ", " + before.author.name + " edited: `" + before.content
        for b_attachment in before.attachments:
            msg = msg + "\n`proxy url: `" + b_attachment.proxy_url
        msg = msg + "\n`to: `" + after.content
        for a_attachment in after.attachments:
            msg = msg + "\n`proxy url: `" + a_attachment.proxy_url
        await channel.send(msg)

modules = ["senpai_fortnite", "senpai_fortune",
           "senpai_imageboards", "senpai_player", "senpai_warframe",
           "senpai_8ball", "senpai_events", "senpai_yugioh", "senpai_polls", "senpai_shop", "senpai_spoiler"]

if (__name__ == "__main__"):

    # amount of arguments
    argc = len(sys.argv)
    # bot token
    token = None

    # map Ctrl+C to trigger signal_handler function
    signal.signal(signal.SIGINT, signal_handler)

    print("Logging in...")

    # parse command line arguments
    for i in range(argc):
        if (sys.argv[i] == "-t" and i < argc):
            token = sys.argv[i+1]
    if (token is None):
        print("Error: no token given")
        sys.exit(1)

    for module in modules:
        bot.load_extension(module)
    bot.run(token)
