# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from rachmaninoff.rachmaninoff_bot import RachmaninoffBot
from rachmaninoff.rachmaninoff_general_cog import RachmaninoffGeneralCog
from rachmaninoff.rachmaninoff_traffic_cog import RachmaninoffTrafficCog
from rachmaninoff.rachmaninoff_weather_cog import RachmaninoffWeatherCog


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')
ALLOWED_USERS = os.getenv('ALLOWED_USERS')
OPENWEATHERMAP_APIKEY = os.getenv('OPENWEATHERMAP_APIKEY')

bot = RachmaninoffBot(command_prefix='!')

bot.add_cog(RachmaninoffTrafficCog(bot=bot, 
                                    mongodb_connection=MONGODB_CONNECTION, 
                                    allowed_users=ALLOWED_USERS))

bot.add_cog(RachmaninoffGeneralCog(bot=bot, allowed_users=ALLOWED_USERS))

bot.add_cog(RachmaninoffWeatherCog(bot=bot, allowed_users=ALLOWED_USERS, openweathermap_apikey=OPENWEATHERMAP_APIKEY))

bot.run(TOKEN)

