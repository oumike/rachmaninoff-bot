# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from rachmaninoff.rachmaninoff_cog import RachmaninoffGeneralCog, RachmaninoffTrafficCog
from rachmaninoff.rachmaninoff_bot import RachmaninoffBot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')
ALLOWED_USERS = os.getenv('ALLOWED_USERS')

bot = RachmaninoffBot(command_prefix='!')

bot.add_cog(RachmaninoffTrafficCog(bot=bot, 
                                    mongodb_connection=MONGODB_CONNECTION, 
                                    allowed_users=ALLOWED_USERS))

bot.add_cog(RachmaninoffGeneralCog(bot=bot, allowed_users=ALLOWED_USERS))

bot.run(TOKEN)

