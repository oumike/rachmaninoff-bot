# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from rachmaninoff_cog import RachmaninoffGeneralCog, RachmaninoffTrafficCog
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')
ALLOWED_USERS = os.getenv('ALLOWED_USERS')

bot = commands.Bot(command_prefix='!')

# bot.add_cog(RachmaninoffGeneralCog(bot))
bot.add_cog(RachmaninoffTrafficCog(bot=bot, 
                                    mongodb_connection=MONGODB_CONNECTION, 
                                    allowed_users=ALLOWED_USERS))

bot.run(TOKEN)