import os
import datetime
import json

import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')


client = discord.Client()

# maybe allow user to pass in an arg to specify their filename
outfile = open(
    "discorpus-"+datetime.datetime.now().date().isoformat()+".json", 'w')

# the structure of the messages in the output json file
def map_message(message):
    return {
        "content": message.content,
        "created_at": message.created_at.timestamp(),
        "is_bot": message.author.bot,
        "author_id": message.author.id,
        "author_name": message.author.name,
        "channel_name": message.channel.name,
        "channel_id": message.channel.id
    }


@client.event
async def on_ready():
    results = []
    # scraping all servers is probably a bad idea, as the bot could potentially be in more than one.
    # maybe add another environment variable to specify which server (which channels?) should be included
    for guild in client.guilds:
        for channel in guild.text_channels:
            counter = 0
            async for message in channel.history(limit=None):
                counter += 1
                if counter % 100 == 0:
                    print(str(counter) +
                          " messages processed so far for " + str(channel))
                mapped_message = map_message(message)
                results.append(mapped_message)
            print("DONE WITH" + str(channel))
    outfile.write(json.dumps(results))
    print("DONE WITH ALL TEXT CHANNELS")

client.run(TOKEN)
