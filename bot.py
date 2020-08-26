# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild)

    # members = '\n - '.join([member.name for member in guild.members])



    

client.run(TOKEN)