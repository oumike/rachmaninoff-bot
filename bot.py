# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from rachmaninoff_cog import RachmaninoffGeneralCog, RachmaninoffTrafficCog
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

bot.add_cog(RachmaninoffGeneralCog(bot))
bot.add_cog(RachmaninoffTrafficCog(bot))

bot.run(TOKEN)