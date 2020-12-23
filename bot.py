# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
from rachmaninoff_bot import RachmaninoffBot
from cogs.general_cog import GeneralCog
from cogs.weather_cog import WeatherCog
from cogs.traffic_cog import TrafficCog
from cogs.covid_cog import CovidCog


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')
ALLOWED_USERS = os.getenv('ALLOWED_USERS')
OPENWEATHERMAP_APIKEY = os.getenv('OPENWEATHERMAP_APIKEY')

bot = RachmaninoffBot(command_prefix='!')

bot.add_cog(TrafficCog(bot=bot, 
                                    mongodb_connection=MONGODB_CONNECTION, 
                                    allowed_users=ALLOWED_USERS))

bot.add_cog(GeneralCog(bot=bot, allowed_users=ALLOWED_USERS))

bot.add_cog(WeatherCog(bot=bot, 
                                    allowed_users=ALLOWED_USERS, 
                                    openweathermap_apikey=OPENWEATHERMAP_APIKEY,
                                    mongodb_connection=MONGODB_CONNECTION))

bot.add_cog(CovidCog(bot=bot, allowed_users=ALLOWED_USERS))

bot.run(TOKEN)

